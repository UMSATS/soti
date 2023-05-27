from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    QUERY_ATTRS,
    SYSTEM_IDS,

    SENDER_ID_MASK,
    DEST_ID_MASK,
    COMM_CODE_MASK,
)

import json, serial, sys, datetime

# first script argument will be the device to read/write to
port_arg = sys.argv[1]

def main_loop():
    with serial.Serial(port_arg, baudrate=115200) as ser:
        json_file = open(MSG_HISTORY_FILENAME)
        while True:
            # block and read indefinitely, reading messages 11 bytes at a time
            new_msg = ser.read(MSG_SIZE)

            comm_code = (new_msg & COMM_CODE_MASK)
            if comm_code in QUERY_ATTRS.keys():
                new_msg_json = {
                    "time": datetime.datetime.now().strftime("%T"),
                    "sender-id": SYSTEM_IDS[(new_msg & SENDER_ID_MASK)],
                    "destination-id": SYSTEM_IDS[(new_msg & DEST_ID_MASK)],
                    "type": QUERY_ATTRS[comm_code]
                    # the remaining attributes are command-specific,
                    # and handled on case-by-case basis
                }

                contents = json.loads(json_file.read())
                contents.append(new_msg_json)
                json_file.write(json.dumps(contents, indent=4))

try:
    main_loop()
except KeyboardInterrupt:
    print("\nTelemetry listener exiting…")
    sys.exit(0)