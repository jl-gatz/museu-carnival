from pathlib import Path


# ---------------------------------------------
# CONFIG (FIXO PARA AS PASTAS DE CONTEÚDO)
# ---------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_DIR = BASE_DIR / "content/md"
OUTPUT_DIR = BASE_DIR / "content/json"
