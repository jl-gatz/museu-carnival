import re


# ----------------------------
# REGEX
# ----------------------------

TIMELINE_REGEX = re.compile(r"[-\s]*?(\d{3,4})\s*(?:\:|\|)\s*([^:]+):\s*(.+)")


# ----------------------------
# CLEANER
# ----------------------------


def clean_timeline_line(line):

    return line.replace("\u00a0", " ").replace("\ufeff", "").strip()


# ----------------------------
# PARSER
# ----------------------------


def parse_timeline_line(line):

    clean_line = clean_timeline_line(line)

    match = TIMELINE_REGEX.match(clean_line)

    if not match:
        return None

    return {
        "ano": match.group(1).strip(),
        "subtitulo": match.group(2).strip(),
        "texto": match.group(3).strip(),
    }
