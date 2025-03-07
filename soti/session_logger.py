"""Parses messages from the input queue."""

import datetime
import os
import string
import struct
from queue import Empty
from enum import Enum
from utils.constants import NodeID, CmdID, SAVE_DATA_DIR, SESSIONS_DIR, SESSION_FILE_FORMAT


def datetime_to_filename(time: datetime):
    file_format = time.strftime(SESSION_FILE_FORMAT)
    return f"{file_format}.log"


def save_log(filename: str, start_time: datetime, end_time: datetime, port, msg_log: str):
    if not os.path.exists(SAVE_DATA_DIR):
        os.mkdir(SAVE_DATA_DIR)
    if not os.path.exists(SESSIONS_DIR):
        os.mkdir(SESSIONS_DIR)

    session_length = end_time - start_time
    hours, remainder = divmod(session_length.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_date = start_time.strftime("%Y-%m-%d")
    formatted_time = start_time.strftime("%H:%M:%S")
    formatted_session_length = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    log_dict = {
        "date": formatted_date,
        "time": formatted_time,
        "session-length": formatted_session_length,
        "port": port,
        "messages": ""
    }

    log_yaml = dict_to_yaml(log_dict, 0)
    log_yaml += msg_log

    with open(SESSIONS_DIR / filename, 'w', encoding="utf_8") as history:
        history.write(log_yaml)


def log_messages(write_msg_queue, stop_flag, port):
    """Writes messages from the queue to the output file."""
    start_time = datetime.datetime.now()
    msg_log = ""

    try:
        while not stop_flag.is_set():
            try:
                new_msg = write_msg_queue.get(block=False)

                new_msg_dict = new_msg.as_dict()
                if new_msg.source == "port":
                    print(f"Message Parsed: {new_msg_dict}")

                # append the new message
                msg_log += dict_to_yaml(new_msg_dict, 1, True) + "\n"

            except Empty: # No item from queue.
                pass
    except KeyboardInterrupt:
        pass

    finally:
        filename = datetime_to_filename(start_time)
        end_time = datetime.datetime.now()
        save_log(filename, start_time, end_time, port, msg_log)


def dict_to_yaml(d: dict, level: int, listItem: bool = False, recursive: bool = False) -> str:
    """Converts a dictionary into a YAML entry."""
    lines = []
    for index, (key, value) in enumerate(d.items()):
        # determine value format based on its type
        if isinstance(value, str) and len(value) > 0:
            value_formatted = value
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
