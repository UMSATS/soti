"""
The SOTI parser.
"""

import re

from .message import Message, MAX_BODY_SIZE
from .constants import NodeID, CmdID
from .value import Value


# Regular Expressions
DATA_ARG_RE = re.compile(r'(?:(\w+)\:)?(\S+)')


class ArgumentException(Exception):
    pass


def get_implied_recipient(cmd: CmdID) -> NodeID | None:
    cmd_name_prefix = cmd.name.split('_')[0]

    match cmd_name_prefix:
        case "CDH":
            return NodeID.CDH
        case "PWR":
            return NodeID.PWR
        case "ADCS":
            return NodeID.ADCS
        case "PLD":
            return NodeID.PLD

    return None


def parse_send(args: str, default_sender: NodeID) -> Message:
    """Parses arguments for the 'send' command.

    Syntax:
    <Command ID> [Optional Data] [Key-Value Options]

    Function Arguments:
    args -- string containing the command arguments.
    default_sender -- the sender ID if none is specified in the command.
    """
    parts = args.split()

    if(len(parts) == 0):
        raise ValueError("No arguments provided")
    try:
        cmd_id = CmdID(Value.from_str(parts[0], 'u8').value)
    except ValueError as e:
        raise ArgumentException(f"Invalid command ID '{parts[0]}': {e}") from e
        
    # Assign default values for the command options.
    priority: int = 255
    sender_id: NodeID = default_sender
    recipient_id: NodeID | None = get_implied_recipient(cmd_id)
    is_ack: bool = False

    # represents the bytes that will be sent in the data section of the message
    data = bytearray()
    data_index = 0

    for arg in parts[1:]:
        try:
            # check if key-value pair
            if '=' in arg:
                key, value = arg.split('=')
                if key == "priority":
                    priority = Value.from_str(value, 'u8').value
                    if not 0 <= priority <= 32:
                        raise ArgumentException(f"Invalid priority '{key}'. Expected range is [0, 32]")
                elif key == "from":
                    try:
                        sender_id = NodeID(Value.from_str(value, 'u8').value)
                    except ValueError as exc:
                        raise ArgumentException(f"Invalid node ID '{value}'") from exc
                elif key == "to":
                    try:
                        recipient_id = NodeID(Value.from_str(value, 'u8').value)
                    except ValueError as exc:
                        raise ArgumentException(f"Invalid node ID '{value}'") from exc
                elif key == "ack":
                    try:
                        is_ack = bool(Value.from_str(value, 'u8').value)
                    except ValueError as exc:
                        raise ArgumentException(f"Invalid value for ack '{value}'. Expected true or false") from exc
                else:
                    raise ArgumentException(f"Unknown option '{key}'")

            # treat as data argument
            elif data_index < MAX_BODY_SIZE:
                re_match = DATA_ARG_RE.match(arg)
                if not re_match:
                    raise ArgumentException(f"Invalid syntax for data argument '{arg}'")

                data_type = re_match.group(1)
                if not data_type:
                    raise ArgumentException(f"You must specify a data type for argument '{arg}'")

                value = Value.from_str(re_match.group(2), data_type)
                raw_bytes = value.to_bytes()

                # Add the bytes of data.
                data.extend(raw_bytes)

        except ValueError as exc:
            raise ArgumentException(f"Invalid argument '{arg}': {exc}") from exc

    if recipient_id is None:
        raise ArgumentException(f"You must specify a recipient with the 'to' option for {cmd_id.name}")

    return Message(
        cmd_id,
        bytes(data),
        255, # Infer body size
        priority,
        sender_id,
        recipient_id,
        is_ack
    )
