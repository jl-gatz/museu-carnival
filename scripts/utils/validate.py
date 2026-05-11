import os
import re
import sys

# ----------------------------
# CONFIG
# ----------------------------

REQUIRED_FRONTMATTER_FIELDS = ["id", "layout", "ano"]
REQUIRED_SECTIONS = ["o_que_e", "por_que_importa", "linha_do_tempo", "curiosidades"]

TIMELINE_REGEX = re.compile(r"^- \d{4}: .+: .+")


# ----------------------------
# HELPERS
# ----------------------------


def split_frontmatter(content):
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    return parts[1].strip(), parts[2].strip()


def parse_frontmatter(frontmatter_str):
    data = {}

    for line in frontmatter_str.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    return data


def extract_sections(content):
    sections = {}
    current_section = None

    for line in content.split("\n"):
        line_stripped = line.strip()

        # Detecta seção ## nome
        if line_stripped.startswith("## "):
            current_section = line_stripped.replace("## ", "").strip()
            sections[current_section] = []
            continue

        if current_section:
            sections[current_section].append(line)

    # Junta o texto
    for key in sections:
        sections[key] = "\n".join(sections[key]).strip()

    return sections


def extract_title_and_linha_fina(content):
    lines = content.split("\n")

    title = None
    linha_fina = None

    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line.replace("# ", "").strip()

            # linha fina deve ser a próxima linha não vazia começando com >
            for j in range(i + 1, len(lines)):
                candidate = lines[j].strip()
                if not candidate:
                    continue
                if candidate.startswith(">"):
                    linha_fina = candidate.replace(">", "").strip()
                break
            break

    return title, linha_fina


# ----------------------------
# VALIDATORS
# ----------------------------


def validate_frontmatter(data):
    errors = []

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in data or not data[field]:
            errors.append(f"Frontmatter: campo obrigatório '{field}' ausente")

    # valida ano
    if "ano" in data:
        if not re.match(r"^\d{4}$", data["ano"]):
            errors.append("Frontmatter: 'ano' deve ser YYYY")

    # valida id kebab-case
    if "id" in data:
        if not re.match(r"^[a-z0-9-]+$", data["id"]):
            errors.append("Frontmatter: 'id' deve estar em kebab-case")

    return errors


def validate_sections(sections):
    errors = []

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"Seção obrigatória ausente: '{section}'")

    return errors


def validate_timeline(timeline_text):
    errors = []

    lines = [l.strip() for l in timeline_text.split("\n") if l.strip()]

    if not lines:
        errors.append("linha_do_tempo: vazia")
        return errors

    for line in lines:
        if not TIMELINE_REGEX.match(line):
            errors.append(f"linha_do_tempo mal formatada: '{line}'")

    return errors


def validate_title_and_linha_fina(title, linha_fina):
    errors = []

    if not title:
        errors.append("Título (# ...) ausente")

    if not linha_fina:
        errors.append("Linha fina (> ...) ausente")

    return errors


# ----------------------------
# CORE
# ----------------------------


def validate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # FRONTMATTER
    frontmatter_str, body = split_frontmatter(content)

    if not frontmatter_str:
        errors.append("Frontmatter ausente")
        frontmatter = {}
    else:
        frontmatter = parse_frontmatter(frontmatter_str)
        errors.extend(validate_frontmatter(frontmatter))

    # TITLE + LINHA FINA
    title, linha_fina = extract_title_and_linha_fina(body)
    errors.extend(validate_title_and_linha_fina(title, linha_fina))

    # SECTIONS
    sections = extract_sections(body)
    errors.extend(validate_sections(sections))

    # TIMELINE
    if "linha_do_tempo" in sections:
        errors.extend(validate_timeline(sections["linha_do_tempo"]))

    return errors


def validate_path(path):
    results = []

    if os.path.isfile(path):
        errors = validate_file(path)
        results.append((path, errors))
        return results

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                errors = validate_file(full_path)
                results.append((full_path, errors))

    return results


# ----------------------------
# CLI
# ----------------------------


def main():
    if len(sys.argv) < 2:
        print("Uso: python validate.py <arquivo.md | pasta>")
        sys.exit(1)

    path = sys.argv[1]
    results = validate_path(path)

    has_error = False

    for filepath, errors in results:
        if not errors:
            print(f"✅ {filepath}")
        else:
            has_error = True
            print(f"\n❌ {filepath}")
            for err in errors:
                print(f"   - {err}")

    if has_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
