# create functions to print out commands' args in appropriate json format,
# then map each one with its corresponding command

def parse_01(args, output):
    output["acknowledged-command"] = f"0x{args[:2]}"
    output["reply-data"] = [f"0x{args[i:i+2]}" for i in range(2, 14, 2)]
    return output

def parse_33(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["well-id"] = int(f"0x{args[2:4]}", 16)
    output["light-level"] = int(f"0x{args[4:8]}", 16)
    return output

def parse_34(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["well-id"] = int(f"0x{args[2:4]}", 16)
    output["temperature"] = int(f"0x{args[4:8]}", 16)
    return output

"""
Parse all other packets.
"""
def parse_generic(args, output):
    output["command"] = f"0x{args[:2]}"
    output["arguments"] = [f"0x{args[i:i+2]}" for i in range(2, 16, 2)]
    return output

parsers = {
    0x01: parse_01,
    0x33: parse_33,
    0x34: parse_34,
}
