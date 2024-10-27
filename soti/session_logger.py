"""Parses messages from the input queue."""

import datetime
import os
import struct
from enum import Enum
from utils.constants import NodeID, CmdID, SAVE_DATA_DIR, SESSIONS_DIR, SESSION_FILE_FORMAT

def init_session_log(port: str) -> str:
    """Initializes the file which logs the session."""
    if not os.path.exists(SAVE_DATA_DIR):
        os.mkdir(SAVE_DATA_DIR)
    if not os.path.exists(SESSIONS_DIR):
        os.mkdir(SESSIONS_DIR)

    session_start = datetime.datetime.now()

    file_format = session_start.strftime(SESSION_FILE_FORMAT)
    file_name = f"{file_format}.log"

    date = session_start.strftime("%Y-%m-%d")
    time = session_start.strftime("%H:%M:%S")

    header_dict = {
        "date": date,
        "time": time,
        "session-length": None,
        "port": port,
        "messages": ""
    }

    header = dict_to_yaml(header_dict, 0)

    with open(SESSIONS_DIR / file_name, 'w', encoding="utf_8") as history:
        history.write(header)

    return file_name

def finalize_session_log(file_name):
    """Writes the session length to the log file."""
    with open(SESSIONS_DIR / file_name, encoding="utf_8") as history:
        log = history.read()

    # get the datetime corresponding to the file name
    session_start = datetime.datetime.strptime(file_name.strip(".log"), SESSION_FILE_FORMAT)

    total_seconds = int((datetime.datetime.now() - session_start).total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # conditionally add hours and format the time
    log = log.split("\n")
    hours_str = f"{hours:02d}:" if hours else ""
    log[2] = f"session-length: '{hours_str}{minutes:02d}:{seconds:02d}'"
    log = "\n".join(log)

    with open(SESSIONS_DIR / file_name, 'w', encoding="utf_8") as history:
        history.write(log)


def log_messages(write_msg_queue, output_file_name):
    """Writes messages from the queue to the output file."""
    while True:
        new_msg = write_msg_queue.get()
        new_msg_dict = new_msg.as_dict()
        if new_msg.source == "port":
            print(f"Message Parsed: {new_msg_dict}")

        with open(SESSIONS_DIR / output_file_name, encoding="utf_8") as history:
            log = history.read()

        log += dict_to_yaml(new_msg_dict, 1, True) + "\n"

        with open(SESSIONS_DIR / output_file_name, 'w', encoding="utf_8") as history:
            history.write(log)


def dict_to_yaml(d: dict, level: int, listItem: bool = False, recursive: bool = False) -> str:
    """Converts a dictionary into a YAML entry."""
    lines = []
    for index, (key, value) in enumerate(d.items()):
        # determine value format based on its type
        if isinstance(value, str) and len(value) > 0:
            value_formatted = f"'{value}'"
        elif isinstance(value, dict):
            if value:
                # handle nested dictionary recursively
                value_formatted = f"\n{dict_to_yaml(value, level + 1, False, True)}"
            else:
                value_formatted = "null"
        elif isinstance(value, Enum):
            value_formatted = value.name
        else:
            # don't apply formatting
            value_formatted = value

        # apply indentation and hyphen
        line = " " * 2 * level
        if listItem and index == 0:
            line = line[:-2] + "- "

        line += f"{key}: {value_formatted}"
        lines.append(line)

    text = "\n".join(lines)
    if not recursive:
        text += "\n"

    return text


def extract_int(data: bytes, index: int, size: int, signed: bool = False) -> int:
    """Extracts an integer of any width from a bytes object."""
    return int.from_bytes(data[index:(size+index)], byteorder='little', signed=signed)


def extract_float(data: bytes, index: int) -> float:
    """Extracts a 32-bit float from a bytes object."""
    return struct.unpack('<f', data[index:(4+index)])[0]


def to_hex_str(data: bytes) -> str:
    """Returns a hexadecimal representation of the provided data."""
    return "0x" + data.hex()


def to_bin_str(data: bytes) -> str:
    """Returns a binary representation of the provided data."""
    bit_string = ''
    for byte in data:
        bits = str(bin(byte))[2:]  # remove '0b' prefix
        bit_string += bits.zfill(8)  # pad with zeros to 8 bits
    return "0b" + bit_string


def parse_msg_body(cmd_id: CmdID, body: bytes) -> dict:
    """Returns relevant data about the provided message."""
    output = {}

    match cmd_id:
        # Common
        case CmdID.COMM_GET_TELEMETRY:
            output['telemetry-key'] = body[0]
        case CmdID.COMM_SET_TELEMETRY_INTERVAL:
            output['telemetry-key'] = body[0]
            output['interval'] = extract_int(body, 1, 2)
        case CmdID.COMM_GET_TELEMETRY_INTERVAL:
            output['telemetry-key'] = body[0]
        case CmdID.COMM_UPDATE_START:
            output['address'] = extract_int(body, 0, 4)
        case CmdID.COMM_UPDATE_LOAD:
            output['data'] = to_hex_str(body)

        # CDH
        case CmdID.CDH_PROCESS_RUNTIME_ERROR:
            output['error-code'] = body[0]
            output['context-code'] = body[1]
            output['debug-data'] = to_hex_str(body[2:7])
        case CmdID.CDH_PROCESS_COMMAND_ERROR:
            output['error-code'] = body[0]
            output['command-id'] = CmdID(body[1])
            output['debug-data'] = to_hex_str(body[2:7])
        case CmdID.CDH_PROCESS_NOTIFICATION:
            output['notification-id'] = body[0]
        case CmdID.CDH_PROCESS_TELEMETRY_REPORT:
            output['telemetry-key'] = body[0]
            output['sequence-number'] = body[1]
            output['packet-number'] = body[2]
            output['telemetry'] = to_hex_str(body[3:7])
        case CmdID.CDH_PROCESS_RETURN:
            output['command-id'] = CmdID(body[0])
            output['data'] = to_hex_str(body[1:7])
        case CmdID.CDH_PROCESS_LED_TEST:
            output['bitmap'] = to_bin_str(body[:2])
        case CmdID.CDH_SET_RTC:
            output['unix-timestamp'] = extract_int(body, 0, 4)
        case CmdID.CDH_RESET_SUBSYSTEM:
            output['subsystem-id'] = NodeID(body[0])

        # Power
        case CmdID.PWR_SET_SUBSYSTEM_POWER:
            output['subsystem-id'] = NodeID(body[0])
            output['power'] = bool(body[1])
        case CmdID.PWR_GET_SUBSYSTEM_POWER:
            output['subsystem-id'] = NodeID(body[0])
        case CmdID.PWR_SET_BATTERY_HEATER_POWER:
            output['heater-power'] = bool(body[0])
        case CmdID.PWR_SET_BATTERY_ACCESS:
            output['battery-access'] = bool(body[0])

        # ADCS
        case CmdID.ADCS_SET_MAGNETORQUER_DIRECTION:
            output['magnetorquer-id'] = body[0]
            output['direction'] = extract_int(body, 1, 1, signed=True)
        case CmdID.ADCS_GET_MAGNETORQUER_DIRECTION:
            output['magnetorquer-id'] = body[0]
        case CmdID.ADCS_SET_OPERATING_MODE:
            output['mode'] = body[0]

        # Payload
        case CmdID.PLD_SET_ACTIVE_ENVS:
            output['bitmap'] = to_bin_str(body[:2])
        case CmdID.PLD_GET_SETPOINT:
            output['well-id'] = body[0]
            output['setpoint'] = extract_float(body, 1)
        case CmdID.PLD_GET_SETPOINT:
            output['well-id'] = body[0]
        case CmdID.PLD_SET_TOLERANCE:
            output['tolerance'] = extract_float(body, 0)

    return output
