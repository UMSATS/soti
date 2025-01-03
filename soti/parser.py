"""
The SOTI parser.
"""

from utils.constants import (
    NodeID, CmdID, DATA_SIZE
)

class ArgumentException(Exception):
    pass


def parse_send(args: str) -> tuple[bytes, str, dict]:
    """Parses arguments for `do_send`."""
    parts = args.split()

    cmd_id = parts[0]
    data = bytearray(DATA_SIZE)
    data_index = 0
    options = {}

    for part in parts[1:]:
        arg = part
        try:
            # check if key-value pair
            if '=' in arg:  
                key, value = arg.split('=')
                options[key] = value

            # treat as data argument
            elif data_index < DATA_SIZE:
                # check if integer type was provided
                explicit_type = arg[0] == "("

                if explicit_type:
                    type_end = arg.find(")")
                    if type_end <= 0: 
                        raise ValueError()

                    type = arg[1 : type_end]

                    # only signed if first character is "i"
                    explicit_sign = not type[0].isnumeric()
                    signed = type[0] == "i" if explicit_sign else False

                    # slice from 1 if sign was provided
                    target_size = int(type[int(explicit_sign):]) // 8

                    # remove the cast from the argument
                    arg = arg[type_end + 1 :]

                negative = arg[0] == "-"
                if negative: 
                    # remove negative sign
                    arg = arg[1:]

                if not explicit_type:
                    # defaults to unsigned unless negative
                    signed = negative

                    # determine minimum byte size to store the number
                    if arg[:2] == "0b":
                        size = (len(arg) - 2 + 7) // 8
                    elif arg[:2] == "0x":
                        size = (len(arg) - 2 + 1) // 2
                    else: # decimal
                        size = (len(format(parse_int(arg), 'x')) + 1) // 2

                    # determine nearest integer width (1, 2, 4 bytes)
                    target_size = 1
                    while target_size < size: target_size *= 2

                # value is the absolute value of the number
                value = parse_int(arg)

                max_unsigned = 2 ** (target_size * 8) - 1
                max_signed = max_unsigned // 2

                # handle overflows based on signedness
                if value > max_unsigned:
                    raise ArgumentException(f"Overflow from {part}")
                elif not signed and negative:
                    raise ArgumentException(f"{part} cannot be unsigned and negative")
                
                elif signed and value > max_signed:
                    if not negative:
                        # overflow to negative two's complement
                        value = value - max_unsigned - 1
                    elif value > max_signed + 1:
                        # negative underflow
                        raise ArgumentException(f"Underflow from {part}")

                if negative:
                    value *= -1

                # create a bytes object
                value = int(value).to_bytes(target_size, byteorder="little", signed=signed)
                # insert the value into data
                end_index = data_index + target_size
                data[data_index : end_index] = value
                data_index = end_index

        except ValueError:
            raise ArgumentException(f"Invalid argument '{part}'")
        except IndexError:
            raise ArgumentException(f"Invalid syntax: {part}")
        except ArgumentException as e:
            raise ArgumentException(e) from e

    # truncate extra bytes
    data = data[:DATA_SIZE]

    return cmd_id, bytes(data), options


def parse_int(i) -> int:
    """
    Casts numbers and enum members to int.
    Raises ValueError for invalid values.
    """
    try:
        if isinstance(i, int):
            return i
        elif isinstance(i, str):
            if i.isnumeric():
                return int(i)
            if i[:2] == "0x":
                return int(i, 16)
            if i[:2] == "0b":
                return int(i, 2)
            if i in NodeID.__members__:
                return NodeID[i].value
            if i in CmdID.__members__:
                return CmdID[i].value
        # no valid cast
        raise ValueError()
    except (ValueError) as e:
        # raises an exception for the caller
        raise ValueError(e) from e
