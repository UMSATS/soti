from cli_utils.constants import MSG_HISTORY_FILENAME, QUERY_ATTRS

import json, serial, sys, datetime

# first script argument will be the device to read/write to
port_arg = sys.argv[1]

def main_loop():
    with serial.Serial(port_arg, baudrate=115200) as ser:
        json_file = open(MSG_HISTORY_FILENAME)
        while True:
            # block and read indefinitely, reading messages 10 bytes at a time
            new_msg = ser.read(10)

            if new_msg[2] in QUERY_ATTRS.keys():
                new_msg_json = {
                    "time": datetime.datetime.now().strftime("%T"),
                    "type": QUERY_ATTRS[new_msg[2]],
                    "value": int(new_msg[3:], 2),
                }

                contents = json.loads(json_file.read())
                contents.append(new_msg_json)
                json_file.write(json.dumps(contents, indent=4))

try:
    main_loop()
except KeyboardInterrupt:
    print("\nTelemetry listener exiting…")
    sys.exit(0)