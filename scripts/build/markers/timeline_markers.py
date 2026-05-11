# ----------------------------
# TIMELINE MARKERS
# ----------------------------

DEBUG_MARKERS = {
    "ano": {"token": "⟦A⟧", "label": "ANO"},
    "subtitulo": {"token": "⟦S⟧", "label": "SUBTITULO"},
    "texto": {"token": "⟦T⟧", "label": "TEXTO"},
}


PRODUCTION_MARKERS = {
    "ano": {"token": "\ue001", "label": "ANO"},
    "subtitulo": {"token": "\ue002", "label": "SUBTITULO"},
    "texto": {"token": "\ue003", "label": "TEXTO"},
}


# ----------------------------
# MODE
# ----------------------------

# Ligar / desligar modo de DEBUG
DEBUG_MODE = True


def mode():
    if DEBUG_MODE:
        return True

    return False


# ----------------------------
# ACTIVE MARKERS
# ----------------------------
def get_timeline_markers():

    if mode():
        return DEBUG_MARKERS

    return PRODUCTION_MARKERS
