def convert_to_hex(input_string):
    if input_string.startswith("0x"):
        return input_string
    elif input_string.startswith("0b"):
        return str(hex(int(input_string, 2)))
    elif input_string.startswith("0o"):
        return str(hex(int(input_string, 8)))
    elif input_string == "\n":
        return "?"

    return str(hex(int(input_string)))