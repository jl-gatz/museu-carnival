import json
from pathlib import Path

from parsers.frontmatter_parser import parse_frontmatter
from parsers.structured_parser import parse_structured


# ----------------------------
# METADATA
# ----------------------------


def resolve_local_image(image_value, md_path):
    """Resolve uma imagem local sem tornar o nome do arquivo uma regra.

    O caminho declarado no frontmatter é preservado quando não existe no
    ambiente atual. Quando o arquivo existe, o JSON recebe um caminho absoluto.
    """

    if not image_value:
        return image_value

    image_text = str(image_value).strip().strip('"').strip("'")

    if image_text.startswith(("http://", "https://")):
        return image_text

    image_path = Path(image_text).expanduser()

    candidates = [image_path]

    if not image_path.is_absolute():
        candidates.insert(0, md_path.parent / image_path)

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate.resolve())

    return image_text


def promote_metadata(data, meta, md_path=None):

    if "ano" in meta:
        try:
            data["ano"] = int(meta["ano"])

        except (ValueError, TypeError):
            data["ano"] = meta["ano"]

    if "id" in meta:
        data["id"] = meta["id"]

    if "layout" in meta:
        data["layout"] = meta["layout"]

    if "numero" in meta:
        data["numero"] = meta["numero"]

    if "imagem" in meta:
        data["imagem"] = (
            resolve_local_image(meta["imagem"], md_path)
            if md_path is not None
            else meta["imagem"]
        )

    return data


# ----------------------------
# PROCESS FILE
# ----------------------------


def process_file(md_path):

    md_path = Path(md_path)

    print("🚨 PROCESSANDO:", md_path)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_frontmatter(content)

    data = parse_structured(body)

    data["meta"] = meta
    data["slug"] = md_path.stem

    data = promote_metadata(data, meta, md_path)

    return data


# ----------------------------
# SAVE DATASET
# ----------------------------


def save_dataset(dataset, output_path):

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"🚀 Dataset gerado: {output_path}")