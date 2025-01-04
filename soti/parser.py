"""
The SOTI parser.
"""

import re
from message import Message
from utils.constants import (
    NodeID, CmdID, COMM_INFO, DATA_SIZE
)

DATA_ARG_RE = re.compile(r'(?:\((\w+)\))?(\S+)')


class ArgumentException(Exception):
    pass


def parse_int(s: str) -> int:
    """
    Casts numbers and enum members to int.
    Raises ValueError for invalid values.
    """
    is_negative = False
    if s[0] == '-':
        is_negative = True
        s = s[1:]

    i: int = 0
    if s.isnumeric():
        i = int(s)
    elif s[:2] == "0x":
        i = int(s, 16)
    elif s[:2] == "0b":
        i = int(s, 2)
    elif s in NodeID.__members__:
        i = NodeID[s].value
    elif s in CmdID.__members__:
        i = CmdID[s].value
    else:
        # no valid parsing
        raise ValueError()

    if is_negative:
        i = -i

    return i


def get_implied_type(value: int) -> str:
    """Uses the range of the integer to infer an appropriate type to store the value."""
    if value < 0:
        if -(2**7) <= value < 2**7:
            return "i8"
        elif -(2**15) <= value < 2**15:
            return "i16"
        elif -(2**31) <= value < 2**31:
            return "i32"
        else:
            raise ValueError(f"{value} is out of range for signed 32-bit integer.")
    else:
        if 0 <= value < 2**8:
            return "u8"
        elif 2**8 <= value < 2**16:
            return "u16"
        elif 2**16 <= value < 2**32:
            return "u32"
        else:
            raise ValueError(f"{value} is out of range for unsigned 32-bit integer.")


def parse_send(args: str, default_sender: NodeID) -> Message:
    """Parses arguments for the 'send' command.

    Syntax:
    <Command ID> [Optional Data] [Key-Value Options]

    Function Arguments:
    args -- string containing the command arguments.
    default_sender -- the sender ID if none is specified in the command.
    """
    parts = args.split()

    try:
        cmd_id = CmdID(parse_int(parts[0]))
    except ValueError:
        raise ArgumentException(f"Invalid command ID {parts[0]}")

    # Assign default values for the command options.
    priority: int = COMM_INFO[cmd_id]["priority"]
    sender_id: NodeID = default_sender
    recipient_id: NodeID | None = COMM_INFO[cmd_id]["dest"]

    # represents the bytes that will be sent in the data section of the message
    data = bytearray()
    data_index = 0

    for arg in parts[1:]:
        try:
            # check if key-value pair
            if '=' in arg:
                key, value = arg.split('=')
                if key == "priority":
                    priority = parse_int(value)
                    if not 0 <= priority <= 32:
                        raise ArgumentException(f"Invalid priority '{key}'. Expected range is [0, 32]")
                elif key == "from":
                    try:
                        sender_id = NodeID(parse_int(value))
                    except ValueError as exc:
                        raise ArgumentException(f"Invalid node ID '{value}'") from exc
                elif key == "to":
                    try:
                        recipient_id = NodeID(parse_int(value))
                    except ValueError as exc:
                        raise ArgumentException(f"Invalid node ID '{value}'") from exc
                else:
                    raise ArgumentException(f"Unknown option '{key}'")

            # treat as data argument
            elif data_index < DATA_SIZE:
                data_type = None
                data_size = 0
                is_signed = False

                re_match = DATA_ARG_RE.match(arg)
                if not re_match:
                    raise ArgumentException(f"Invalid syntax for data argument '{arg}'")

                data_type = re_match.group(1)
                value = parse_int(re_match.group(2))

                if not data_type:
                    data_type = get_implied_type(value)

                if data_type in ["u8", "u16", "u32"]:
                    is_signed = False
                elif data_type in ["i8", "i16", "i32"]:
                    is_signed = True

                if data_type in ["u8", "i8"]:
                    data_size = 1
                elif data_type in ["u16", "i16"]:
                    data_size = 2
                elif data_type in ["u32", "i32"]:
                    data_size = 4

                # create a bytes object
                data.extend(value.to_bytes(data_size, byteorder="little", signed=is_signed))

        except ValueError as exc:
            raise ArgumentException(f"Invalid argument '{arg}': {exc}") from exc

    if recipient_id is None:
        raise ArgumentException(f"You must specify a recipient with the 'to' option for {cmd_id.name}")

    # Ensure the data field is the correct length.
    if len(data) > DATA_SIZE:
        data = data[:DATA_SIZE]  # Truncate to the right length.
    elif len(data) < DATA_SIZE:
        data = data + bytearray(DATA_SIZE - len(data))  # Extend with zeroes.

    return Message(priority, sender_id, recipient_id, cmd_id, bytes(data), source="user")
