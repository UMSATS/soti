from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    QUERY_ATTRS,
    SYSTEM_IDS
)

from cli_utils.command_args import parsers, parse_generic

from shared_queue import msg_queue

import json, serial, sys, datetime, queue

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

    new_msg_json = {
        "time": datetime.datetime.now().strftime("%T"),
        "priority": int(f"0x{msg[2:4]}", 16),
        "sender-id": SYSTEM_IDS[int(f"0x{msg[4:6]}", 16)],
        "destination-id": SYSTEM_IDS[int(f"0x{msg[6:8]}", 16)],
        "type": QUERY_ATTRS.get(comm_code) or "other-message",
        # the remaining attributes are command-specific,
        # and handled on case-by-case basis
    }

    if new_msg_json["type"] == "other-message":
        new_msg_json["command-code"] = f"0x{msg[8:10]}"

    if comm_code in parsers.keys():
        new_msg_json = parsers[comm_code](msg[10:], new_msg_json)
    else:
        new_msg_json = parse_generic(msg[10:], new_msg_json)

    return new_msg_json

def init_json():
    with open(MSG_HISTORY_FILENAME, "r+") as history:
        if not history.read():
            history.write("[]")

def parse_msg():
    while True:
        try:
            new_msg_raw = msg_queue.get()
            new_msg_json = parse(msg_queue.get())

            print(f"Message Parsed: {new_msg_json}")

            if new_msg_json:
                with open(MSG_HISTORY_FILENAME) as history:
                    contents = json.load(history)
                    contents.append(new_msg_json)
                with open(MSG_HISTORY_FILENAME, 'w') as history:
                    json.dump(contents, history, indent=4)
        except msg_queue.empty():
            pass

if __name__ == "__main__":
    init_json()
    parse_msg()