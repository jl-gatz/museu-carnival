def handle_curiosidades(line, data):

    if not line.startswith("- "):
        return

    data["curiosidades"]["itens"].append(line[2:].strip())
