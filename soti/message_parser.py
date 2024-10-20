"""Parses messages from the input queue."""

import datetime
import struct
from enum import Enum
from utils.constants import NodeID, CmdID, SESSIONS_DIR

class Message:
    def __init__(self, msg_bytes: bytes, source: str):
        """Initialize the message from a bytes object."""
        self.bytes = msg_bytes
        # serial parameters
        self.priority = msg_bytes[0]
        self.sender = NodeID(msg_bytes[1])
        self.recipient = NodeID(msg_bytes[2])
        self.cmd_id = CmdID(msg_bytes[3])
        self.body = msg_bytes[4:]
        # additional parameters
        self.time = datetime.datetime.now().strftime("%T")
        self.source = source
        
    def as_dict(self) -> dict:
        """Return the message parameters as a dictionary."""
        return {
            "time": self.time,
            "source": self.source,
            "priority": self.priority,
            "sender-id": self.sender,
            "recipient-id": self.recipient,
            "cmd": self.cmd_id,
            "body": parse_msg_body(self.cmd_id, self.body)
        }


def log_messages(write_msg_queue, output_file_name):
    """Writes messages from the queue to the output file."""
    while True:
        new_msg = write_msg_queue.get()
        new_msg_dict = new_msg.as_dict()
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
        bits = bin(byte)[2:]  # remove '0b' prefix
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
