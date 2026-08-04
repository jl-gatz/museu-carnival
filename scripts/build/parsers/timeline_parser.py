import re


# ----------------------------
# REGEX
# ----------------------------
TIMELINE_RE = re.compile(
    r"^\s*[-*+]\s+(?P<ano>\d{4})\s*\|\s*(?P<subtitulo>[^:]+?)\s*:\s*(?P<texto>.+?)\s*$"
)


# ----------------------------
# CLEANER
# ----------------------------


def clean_timeline_line(line):

    return line.replace("\u00a0", " ").replace("\ufeff", "").strip()


# ----------------------------
# PARSER
# ----------------------------


def parse_timeline_line(line):
    match = TIMELINE_RE.match(line)

    if not match:
        return None

    ano = match.group("ano").strip()
    subtitulo = match.group("subtitulo")
    texto = match.group("texto").strip()

    return {
        "ano": ano,
        "subtitulo": subtitulo.strip() if subtitulo else "",
        "texto": texto,
    }
