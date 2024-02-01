# create functions to print out commands' args in appropriate json format,
# then map each one with its corresponding command

def parse_01(args, output):
    output["acknowledged-command"] = f"0x{args[:2]}"
    # Data is stored as a list so that camera data can be easily processed.
    output["reply-data"] = [f"0x{args[i:i+2]}" for i in range(2, 14, 2)]
    return output

def parse_30(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["battery-charge"] = int(f"0x{args[2:10]}", 16)
    return output

def parse_31(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["battery-temperature"] = int(f"0x{args[2:6]}", 16)
    return output

def parse_32(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["current-sensor-id"] = int(f"0x{args[2:4]}", 16)
    output["current-consumption"] = int(f"0x{args[4:8]}", 16)
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

def parse_35(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["quaternion-i-component"] = int(f"0x{args[2:6]}", 16)
    output["quaternion-j-component"] = int(f"0x{args[6:10]}", 16)
    output["quaternion-k-component"] = int(f"0x{args[10:14]}", 16)
    return output

def parse_36(args, output):
    output["telemetry-sequence-number"] = int(f"0x{args[:2]}", 16)
    output["quaternion-real-component"] = int(f"0x{args[2:6]}", 16)
    output["measurement-accuracy"] = int(f"0x{args[6:10]}", 16)
    return output

"""
Parse all other packets.
"""
def parse_generic(args, output):
    output["command"] = f"0x{args[:2]}"
    output["arguments"] = f"0x{args[2:]}"
    return output

parsers = {
    0x01: parse_01,
    0x30: parse_30,
    0x31: parse_31,
    0x32: parse_32,
    0x33: parse_33,
    0x34: parse_34,
    0x35: parse_35,
    0x36: parse_36,
}
