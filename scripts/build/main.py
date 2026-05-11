import sys

from pathlib import Path

from config.settings import INPUT_DIR, OUTPUT_DIR

from services.dataset_builder import process_file, save_dataset


# ----------------------------
# MAIN
# ----------------------------


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = []

    print("🚨 SCRIPT DE CONVERSÃO Móðguðr")

    # ----------------------------
    # ARGUMENTOS
    # ----------------------------

    input_arg = sys.argv[1] if len(sys.argv) > 1 else None

    # ----------------------------
    # OUTPUT NAME
    # ----------------------------

    if len(sys.argv) > 2:
        # nome explícito
        output_arg = sys.argv[2]

    elif input_arg:
        # usa nome do arquivo de entrada
        output_arg = f"{Path(input_arg).stem}.json"

    else:
        # fallback modo lote
        output_arg = "dataset.json"

    output_path = OUTPUT_DIR / output_arg

    # ----------------------------
    # ARQUIVO ÚNICO
    # ----------------------------

    if input_arg:
        input_path = Path(input_arg).resolve()

        if not input_path.is_file():
            print("❌ Arquivo não encontrado.")
            return

        data = process_file(input_path)

        if data:
            dataset.append(data)

    # ----------------------------
    # MODO LOTE
    # ----------------------------

    else:
        for md_file in INPUT_DIR.glob("*.md"):
            data = process_file(md_file)

            if data:
                dataset.append(data)

    # ----------------------------
    # SAVE
    # ----------------------------

    save_dataset(dataset, output_path)


if __name__ == "__main__":
    main()
