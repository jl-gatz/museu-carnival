from markers.timeline_markers import get_timeline_markers


# ----------------------------
# TIMELINE MARKERS
# ----------------------------
TIMELINE_MARKERS = get_timeline_markers()


def marker(name):
    return TIMELINE_MARKERS[name]["token"]


# ----------------------------
# RENDER DA TIMELINE
# ----------------------------
def render_timeline_markup(items):

    blocks = []

    for item in items:
        blocks.append(
            f"{marker('ano')}{item['ano']} "
            f"{marker('subtitulo')}{item['subtitulo']}\r"
            f"\t{marker('texto')}{item['texto']}"
        )

    return "\r".join(blocks)
