from renders.timeline_renderer import render_timeline_markup
from utils.normalizer import normalize

from parsers.handlers.timeline_section import handle_timeline
from parsers.handlers.curiosidades_section import handle_curiosidades


# ----------------------------
# SECTION HANDLERS
# ----------------------------

SECTION_HANDLERS = {
    "linha_do_tempo": handle_timeline,
    "curiosidades": handle_curiosidades,
}


# ----------------------------
# PARSE DOS DADOS
# ----------------------------


def parse_structured(content):

    lines = content.splitlines()

    data = {
        "titulo": "",
        "linha_fina": "",
        "o_que_e": {"titulo": "O que é?", "texto": ""},
        "por_que_importa": {"titulo": "Por que importa?", "texto": ""},
        "linha_do_tempo": {"titulo": "Linha do tempo", "itens": []},
        "curiosidades": {"titulo": "Curiosidades", "itens": []},
        "curiosidade_destaque": {"titulo": "", "texto": ""},
        "explore_mais": {"titulo": "Explore mais", "texto": ""},
    }

    current_section = None
    buffer = []

    # ----------------------------
    # FLUSH BUFFER
    # ----------------------------

    def append_paragraph(section, field, text):
        current_text = data[section][field]
        data[section][field] = (
            current_text + "\r" + text if current_text else text
        )

    def flush_buffer():

        nonlocal buffer, current_section

        text = " ".join(buffer).strip()

        if not text:
            buffer = []
            return

        if current_section == "linha_fina":
            data["linha_fina"] = (
                data["linha_fina"] + " " + text
                if data["linha_fina"]
                else text
            )

        elif current_section == "o_que_e":
            append_paragraph("o_que_e", "texto", text)

        elif current_section == "por_que_importa":
            append_paragraph("por_que_importa", "texto", text)

        elif current_section == "curiosidade_destaque":
            append_paragraph("curiosidade_destaque", "texto", text)

        elif current_section == "explore_mais":
            append_paragraph("explore_mais", "texto", text)

        buffer = []

    # ----------------------------
    # LOOP PRINCIPAL
    # ----------------------------

    for line in lines:
        line = line.strip()

        # ----------------------------
        # TÍTULO
        # ----------------------------

        if line.startswith("# "):
            data["titulo"] = line[2:]
            current_section = None

        # ----------------------------
        # LINHA FINA
        # ----------------------------

        elif line.startswith("> "):
            data["linha_fina"] = line[2:].strip()

        # ----------------------------
        # SEÇÕES
        # ----------------------------

        elif line.startswith("## "):
            flush_buffer()

            section = normalize(line[3:])

            valid_sections = [
                "o_que_e",
                "por_que_importa",
                "linha_do_tempo",
                "curiosidades",
                "curiosidade_destaque",
                "explore_mais",
            ]

            current_section = section if section in valid_sections else None

        # ----------------------------
        # SUBTÍTULO DA CURIOSIDADE EM DESTAQUE
        # ----------------------------

        elif (
            line.startswith("### ")
            and current_section == "curiosidade_destaque"
        ):
            flush_buffer()
            data["curiosidade_destaque"]["titulo"] = line[4:].strip()

        # ----------------------------
        # SECTION HANDLERS
        # ----------------------------

        elif current_section in SECTION_HANDLERS:
            SECTION_HANDLERS[current_section](line, data)

        # ----------------------------
        # PARÁGRAFOS
        # ----------------------------

        elif line == "":
            flush_buffer()

        else:
            if current_section is None:
                current_section = "linha_fina"

            buffer.append(line)

    # ----------------------------
    # FLUSH FINAL
    # ----------------------------

    flush_buffer()

    # ----------------------------
    # TIMELINE MARKUP
    # ----------------------------

    data["linha_do_tempo"]["markup"] = render_timeline_markup(
        data["linha_do_tempo"]["itens"]
    )

    return data
