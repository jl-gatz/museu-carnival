# Parse para a primeira extração de conteúdo e metadados


def parse_frontmatter(content):
    """
    Extrai bloco --- YAML-like simples
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    raw_meta = parts[1]
    body = parts[2]

    meta = {}
    for line in raw_meta.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    return meta, body.strip()
