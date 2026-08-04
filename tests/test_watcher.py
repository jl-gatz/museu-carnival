import importlib
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


def import_watcher_without_dependency():
    watchdog = types.ModuleType("watchdog")
    events = types.ModuleType("watchdog.events")
    observers = types.ModuleType("watchdog.observers")
    polling = types.ModuleType("watchdog.observers.polling")

    class FileSystemEventHandler:
        pass

    class Observer:
        pass

    events.FileSystemEventHandler = FileSystemEventHandler
    observers.Observer = Observer
    polling.PollingObserver = Observer

    modules = {
        "watchdog": watchdog,
        "watchdog.events": events,
        "watchdog.observers": observers,
        "watchdog.observers.polling": polling,
    }
    with patch.dict(sys.modules, modules):
        return importlib.import_module("watcher")


watcher = import_watcher_without_dependency()


class WatcherTests(unittest.TestCase):
    def test_ignores_temporary_and_non_markdown_files(self):
        self.assertTrue(watcher.is_markdown(Path("equipamento.md")))
        self.assertFalse(watcher.is_markdown(Path(".equipamento.md")))
        self.assertFalse(watcher.is_markdown(Path("~equipamento.md")))
        self.assertFalse(watcher.is_markdown(Path("equipamento.md~")))
        self.assertFalse(watcher.is_markdown(Path("equipamento.txt")))

    def test_processes_one_material_using_current_json_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "content/md"
            output_dir = root / "content/json"
            error_dir = root / "producao/erros"
            input_dir.mkdir(parents=True)

            md_path = input_dir / "equipamento.md"
            md_path.write_text("conteúdo", encoding="utf-8")
            processor = watcher.MarkdownProcessor(input_dir, output_dir, error_dir)

            parsed = {"id": "equipamento", "titulo": "Equipamento"}
            with patch.object(watcher, "process_file", return_value=parsed):
                self.assertTrue(processor.process(md_path))

            payload = json.loads(
                (output_dir / "equipamento.json").read_text(encoding="utf-8")
            )
            self.assertEqual(payload, [parsed])

    def test_parser_error_preserves_previous_json_and_writes_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "content/md"
            output_dir = root / "content/json"
            error_dir = root / "producao/erros"
            input_dir.mkdir(parents=True)
            output_dir.mkdir(parents=True)

            md_path = input_dir / "equipamento.md"
            md_path.write_text("inválido", encoding="utf-8")
            json_path = output_dir / "equipamento.json"
            previous = '[{"versao": "anterior"}]\n'
            json_path.write_text(previous, encoding="utf-8")
            processor = watcher.MarkdownProcessor(input_dir, output_dir, error_dir)

            with patch.object(watcher, "process_file", side_effect=ValueError("falha")):
                self.assertFalse(processor.process(md_path))

            self.assertEqual(json_path.read_text(encoding="utf-8"), previous)
            report = (error_dir / "equipamento.error.log").read_text(encoding="utf-8")
            self.assertIn("ValueError: falha", report)
            self.assertIn("Saída preservada", report)

    def test_pending_scan_skips_current_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "content/md"
            output_dir = root / "content/json"
            error_dir = root / "producao/erros"
            input_dir.mkdir(parents=True)
            output_dir.mkdir(parents=True)

            md_path = input_dir / "equipamento.md"
            md_path.write_text("conteúdo", encoding="utf-8")
            json_path = output_dir / "equipamento.json"
            json_path.write_text("[]\n", encoding="utf-8")
            newer = md_path.stat().st_mtime_ns + 10_000_000
            json_path.touch()
            # Garante a relação de datas sem depender da resolução do filesystem.
            import os

            os.utime(json_path, ns=(newer, newer))
            processor = watcher.MarkdownProcessor(input_dir, output_dir, error_dir)

            with patch.object(processor, "process") as process:
                counts = processor.process_pending()

            self.assertEqual(counts, (0, 0, 1))
            process.assert_not_called()


if __name__ == "__main__":
    unittest.main()
