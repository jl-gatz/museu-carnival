"""Observa a pasta de Markdown e mantém os JSONs correspondentes atualizados.

O módulo detecta arquivos criados, alterados ou movidos para ``content/md``.
Cada Markdown é convertido pelo mesmo ``DatasetBuilder`` usado pelo comando
manual. A saída é gravada atomicamente para que o InDesign nunca encontre um
JSON incompleto.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    from watchdog.observers.polling import PollingObserver
except ImportError as exc:  # pragma: no cover - depende do ambiente de execução
    raise SystemExit(
        "A dependência 'watchdog' não está instalada. "
        "Execute: 'poetry install' na raiz do projeto"
    ) from exc

from config.settings import BASE_DIR, INPUT_DIR, OUTPUT_DIR
from services.dataset_builder import process_file


LOGGER = logging.getLogger("museu.watcher")

IGNORED_SUFFIXES = {
    ".bak",
    ".part",
    ".swp",
    ".temp",
    ".tmp",
}


def is_markdown(path: Path) -> bool:
    """Retorna ``True`` somente para Markdown que não parece temporário."""

    name = path.name
    if path.suffix.lower() != ".md":
        return False
    if name.startswith((".", "~", "#")) or name.endswith(("~", "#")):
        return False
    return not any(name.lower().endswith(suffix) for suffix in IGNORED_SUFFIXES)


def atomic_write_json(payload: object, destination: Path) -> None:
    """Grava JSON no mesmo volume e o publica com uma troca atômica."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{destination.stem}.",
            suffix=".tmp",
            dir=destination.parent,
            delete=False,
        ) as temporary:
            json.dump(payload, temporary, indent=2, ensure_ascii=False)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name

        os.replace(temporary_name, destination)
    finally:
        if temporary_name:
            temporary_path = Path(temporary_name)
            if temporary_path.exists():
                temporary_path.unlink()


def atomic_write_text(content: str, destination: Path) -> None:
    """Publica um relatório textual sem deixar arquivos parciais."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{destination.stem}.",
            suffix=".tmp",
            dir=destination.parent,
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name

        os.replace(temporary_name, destination)
    finally:
        if temporary_name:
            temporary_path = Path(temporary_name)
            if temporary_path.exists():
                temporary_path.unlink()


class MarkdownProcessor:
    """Converte um Markdown e administra sua saída e seu relatório de erro."""

    def __init__(self, input_dir: Path, output_dir: Path, error_dir: Path):
        self.input_dir = input_dir.resolve()
        self.output_dir = output_dir.resolve()
        self.error_dir = error_dir.resolve()

    def relative_path(self, md_path: Path) -> Path:
        try:
            return md_path.resolve().relative_to(self.input_dir)
        except ValueError as exc:
            raise ValueError(f"Arquivo fora da pasta observada: {md_path}") from exc

    def output_path(self, md_path: Path) -> Path:
        return (self.output_dir / self.relative_path(md_path)).with_suffix(".json")

    def error_path(self, md_path: Path) -> Path:
        relative = self.relative_path(md_path)
        return (self.error_dir / relative).with_suffix(".error.log")

    def process(self, md_path: Path) -> bool:
        md_path = md_path.resolve()
        if not is_markdown(md_path) or not md_path.is_file():
            return False

        output_path = self.output_path(md_path)
        error_path = self.error_path(md_path)
        LOGGER.info("[DETECTADO] %s", self.relative_path(md_path))

        try:
            data = process_file(md_path)
            if not data:
                raise ValueError("O parser não retornou conteúdo.")

            # Um arquivo por material, preservando o contrato atual do JSX:
            # a raiz do JSON continua sendo uma lista com um item.
            atomic_write_json([data], output_path)
        except Exception as exc:  # mantém o watcher vivo após erros editoriais
            report = (
                f"Arquivo: {md_path}\n"
                f"Saída preservada: {output_path}\n"
                f"Erro: {type(exc).__name__}: {exc}\n\n"
                f"{traceback.format_exc()}"
            )
            atomic_write_text(report, error_path)
            LOGGER.error("[ERRO] %s: %s", self.relative_path(md_path), exc)
            return False

        if error_path.exists():
            error_path.unlink()
        LOGGER.info("[OK] %s -> %s", self.relative_path(md_path), output_path)
        return True

    def process_pending(self, force: bool = False) -> tuple[int, int, int]:
        """Converte entradas novas/alteradas e informa processadas, erros e atuais."""

        processed = 0
        errors = 0
        current = 0

        for md_path in sorted(self.input_dir.rglob("*.md")):
            if not is_markdown(md_path):
                continue

            output_path = self.output_path(md_path)
            pending = (
                force
                or not output_path.exists()
                or md_path.stat().st_mtime_ns > output_path.stat().st_mtime_ns
            )
            if not pending:
                current += 1
                continue

            if self.process(md_path):
                processed += 1
            else:
                errors += 1

        return processed, errors, current


class MarkdownEventHandler(FileSystemEventHandler):
    """Agrupa eventos repetidos e espera o arquivo terminar de ser gravado."""

    def __init__(
        self,
        processor: MarkdownProcessor,
        debounce_seconds: float = 0.8,
        stability_seconds: float = 0.4,
        stability_checks: int = 3,
    ):
        super().__init__()
        self.processor = processor
        self.debounce_seconds = debounce_seconds
        self.stability_seconds = stability_seconds
        self.stability_checks = stability_checks
        self._timers: dict[Path, threading.Timer] = {}
        self._generations: dict[Path, int] = {}
        self._lock = threading.Lock()

    def on_created(self, event) -> None:
        if not event.is_directory:
            self.schedule(Path(event.src_path))

    def on_modified(self, event) -> None:
        if not event.is_directory:
            self.schedule(Path(event.src_path))

    def on_moved(self, event) -> None:
        if not event.is_directory:
            self.schedule(Path(event.dest_path))

    def on_deleted(self, event) -> None:
        if event.is_directory:
            return
        deleted_path = Path(event.src_path)
        if is_markdown(deleted_path):
            LOGGER.warning(
                "[ATENÇÃO] Markdown removido; o JSON foi preservado: %s",
                deleted_path.name,
            )

    def schedule(self, path: Path) -> None:
        path = path.resolve()
        if not is_markdown(path):
            return

        with self._lock:
            previous = self._timers.pop(path, None)
            if previous:
                previous.cancel()

            generation = self._generations.get(path, 0) + 1
            self._generations[path] = generation
            timer = threading.Timer(
                self.debounce_seconds,
                self._process_when_stable,
                (path, generation),
            )
            timer.daemon = True
            self._timers[path] = timer
            timer.start()

    def _process_when_stable(self, path: Path, generation: int) -> None:
        try:
            if self._wait_until_stable(path, generation):
                self.processor.process(path)
        finally:
            with self._lock:
                if self._generations.get(path) == generation:
                    self._timers.pop(path, None)
                    self._generations.pop(path, None)

    def _wait_until_stable(self, path: Path, generation: int) -> bool:
        previous_fingerprint: tuple[int, int] | None = None
        stable_count = 0

        while stable_count < self.stability_checks:
            with self._lock:
                if self._generations.get(path) != generation:
                    return False

            try:
                stat = path.stat()
            except FileNotFoundError:
                return False

            fingerprint = (stat.st_size, stat.st_mtime_ns)
            if fingerprint == previous_fingerprint:
                stable_count += 1
            else:
                previous_fingerprint = fingerprint
                stable_count = 0

            time.sleep(self.stability_seconds)

        return True

    def cancel_pending(self) -> None:
        with self._lock:
            for timer in self._timers.values():
                timer.cancel()
            self._timers.clear()
            self._generations.clear()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Converte automaticamente Markdown do museu em JSON.",
    )
    parser.add_argument("--input", type=Path, default=INPUT_DIR, help="Pasta de Markdown.")
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR, help="Pasta de JSON.")
    parser.add_argument(
        "--errors",
        type=Path,
        default=BASE_DIR / "producao/erros",
        help="Pasta dos relatórios de erro.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Converte pendências e encerra, sem observar a pasta.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reconverte todos os Markdown na varredura inicial.",
    )
    parser.add_argument(
        "--polling",
        action="store_true",
        help="Usa varredura periódica em vez de eventos nativos.",
    )
    parser.add_argument("--debounce", type=float, default=0.8, help="Debounce em segundos.")
    parser.add_argument(
        "--stability-interval",
        type=float,
        default=0.4,
        help="Intervalo entre verificações de estabilidade.",
    )
    parser.add_argument(
        "--stability-checks",
        type=int,
        default=3,
        help="Número de verificações estáveis antes de converter.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    input_dir = args.input.resolve()
    output_dir = args.output.resolve()
    error_dir = args.errors.resolve()

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    error_dir.mkdir(parents=True, exist_ok=True)

    processor = MarkdownProcessor(input_dir, output_dir, error_dir)
    processed, errors, current = processor.process_pending(force=args.force)
    LOGGER.info(
        "[INICIAL] %s convertido(s), %s erro(s), %s já atualizado(s).",
        processed,
        errors,
        current,
    )

    if args.once:
        return 1 if errors else 0

    handler = MarkdownEventHandler(
        processor,
        debounce_seconds=args.debounce,
        stability_seconds=args.stability_interval,
        stability_checks=args.stability_checks,
    )
    observer = PollingObserver() if args.polling else Observer()
    observer.schedule(handler, str(input_dir), recursive=True)
    observer.start()
    LOGGER.info("[OBSERVANDO] %s", input_dir)

    try:
        while observer.is_alive():
            observer.join(timeout=1)
    except KeyboardInterrupt:
        LOGGER.info("[ENCERRANDO] Interrupção solicitada pelo usuário.")
    finally:
        handler.cancel_pending()
        observer.stop()
        observer.join()

    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    args = build_parser().parse_args(argv)

    if args.debounce < 0 or args.stability_interval <= 0 or args.stability_checks < 1:
        LOGGER.error("Intervalos inválidos: use valores positivos para estabilidade.")
        return 2

    return run(args)


if __name__ == "__main__":
    sys.exit(main())
