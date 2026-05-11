from parsers.timeline_parser import parse_timeline_line


def handle_timeline(line, data):

    timeline_item = parse_timeline_line(line)

    if not timeline_item:
        return

    data["linha_do_tempo"]["itens"].append(timeline_item)
