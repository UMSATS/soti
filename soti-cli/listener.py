from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    QUERY_ATTRS,
    SYSTEM_IDS
)

from cli_utils.command_args import parsers

import json, serial, sys, datetime

def bytes_to_string(msg):
    result = "0x"
    for byte in msg:
        bytestring = str(hex(byte))[2:]
        if len(bytestring) < 2:
            result += "0"
        result += bytestring
    return result

def parse(msg_raw):
    msg = bytes_to_string(msg_raw)
    comm_code = int(f"0x{msg[8:10]}", 16)

    if comm_code in QUERY_ATTRS.keys():
        new_msg_json = {
            "time": datetime.datetime.now().strftime("%T"),
            "sender-id": SYSTEM_IDS[int(f"0x{msg[4:6]}", 16)],
            "destination-id": SYSTEM_IDS[int(f"0x{msg[6:8]}", 16)],
            "type": QUERY_ATTRS[comm_code]
            # the remaining attributes are command-specific,
            # and handled on case-by-case basis
        }

        if comm_code in parsers.keys():
            new_msg_json = parsers[comm_code](msg[10:], new_msg_json)

        return new_msg_json
    return None

# first script argument will be the device to read/write to
port_arg = sys.argv[1]

def init_json():
    with open(MSG_HISTORY_FILENAME, "r+") as history:
        if not history.read():
            history.write("[]")

def main_loop():
    with serial.Serial(port_arg, baudrate=115200) as ser:
        while True:
            # block and read indefinitely, reading messages 11 bytes at a time
            new_msg = ser.read(MSG_SIZE)

            new_msg_json = parse(new_msg)
            if new_msg_json:
                with open(MSG_HISTORY_FILENAME) as history:
                    contents = json.load(history)
                    contents.append(new_msg_json)
                with open(MSG_HISTORY_FILENAME, 'w') as history:
                    json.dump(contents, history, indent=4)

try:
    init_json()
    main_loop()
except KeyboardInterrupt:
    print("\nTelemetry listener exiting…")
    sys.exit(0)