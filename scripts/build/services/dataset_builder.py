import json

from parsers.frontmatter_parser import parse_frontmatter
from parsers.structured_parser import parse_structured


# ----------------------------
# METADATA
# ----------------------------


def promote_metadata(data, meta):

    if "ano" in meta:
        try:
            data["ano"] = int(meta["ano"])

        except ValueError:
            data["ano"] = meta["ano"]

    if "id" in meta:
        data["id"] = meta["id"]

    if "layout" in meta:
        data["layout"] = meta["layout"]

    if "numero" in meta:
        data["numero"] = meta["numero"]

    return data


# ----------------------------
# PROCESS FILE
# ----------------------------


def process_file(md_path):

    print("🚨 PROCESSANDO:", md_path)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_frontmatter(content)

    data = parse_structured(body)

    data["meta"] = meta
    data["slug"] = md_path.stem

    data = promote_metadata(data, meta)

    return data


# ----------------------------
# SAVE DATASET
# ----------------------------


def save_dataset(dataset, output_path):

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"🚀 Dataset gerado: {output_path}")
