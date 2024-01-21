def parse_input(input: str) -> (str, str | None):
    # if input is in format: "start_station (line)", then parse start_station and line
    input = input.strip()
    input = input.lower()
    input = input.split('(')

    start_station = input[0].strip()
    start_line = None

    if len(input) > 1:
        start_line = input[1].strip()
        # get rid of parentheses

        start_line = start_line.replace('(', '')
        start_line = start_line.replace(')', '')

    return start_station, start_line

    