"""
The main soti front-end script which initializes the terminal and listener threads.
"""

import multiprocessing
import cmd
import serial.tools.list_ports
import serial.tools.list_ports_common

from utils import help_strings
from utils.constants import (
    NodeID, CmdID, COMM_INFO, DATA_SIZE
)

from serial_reader import serial_reader
from session_logger import log_messages
from message import Message


class ArgumentException(Exception): pass

# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class CommandLine(cmd.Cmd):
    """Represents the command line interface."""
    # initialize the object
    def __init__(self, out_queue, write_queue):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\niamnow\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_queue
        self.write_msg_queue = write_queue
        self.sender_id = NodeID.CDH


    def do_send(self, arg):
        """Sends a command."""
        try:
            cmd_str, data, options = parse_send(arg)
            
            # get corresponding CmdID
            try:
                cmd_id = CmdID(parse_int(cmd_str))
            except ValueError:
                raise ArgumentException("Invalid command ID")

            # get the default values for the command
            priority = COMM_INFO[cmd_id]["priority"]
            sender_id = self.sender_id
            dest_id = COMM_INFO[cmd_id]["dest"]
            
            # override defaults with optional arguments
            for key in options:
                if key == "priority":
                    priority = parse_int(options["priority"])
                
                try:
                    if key == "from":
                        sender_id = NodeID(parse_int(options["from"]))
                    if key == "to":
                        dest_id = NodeID(parse_int(options["to"]))
                except (ValueError, KeyError):
                    raise ArgumentException("Invalid node ID")
            
            # raise exceptions for invalid arguments
            if not (0 <= priority <= 32):
                raise ArgumentException("Invalid priority")
            
            if dest_id is None:
                raise ArgumentException(f"{cmd_id.name} requires a recipient")

            print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.get_display_name()}")

            # create a message using the arguments
            msg = Message(priority, sender_id, dest_id, cmd_id, data, source="user")

            # send the message to be written to the serial device and logged
            self.write_msg_queue.put(msg)
            self.out_msg_queue.put(msg)

        except (ValueError, ArgumentException) as e:
            print(e)
            return


    def do_iamnow(self, arg):
        """Changes the default sender ID."""
        try:
            node_id = NodeID(parse_int(arg))
            if node_id in NodeID:
                self.sender_id = node_id
                print(f"Updated sender ID to {self.sender_id.get_display_name()}.")
            else:
                print("Invalid sender ID.")
        except ValueError:
            print("Invalid args.")


    def do_help(self, arg):
        """Displays help messages."""
        if arg == "send":
            cmd_method = getattr(self, "do_send")
            print(f"Description: {cmd_method.__doc__}")
            print(f"Usage: send <command> [data1 ...] [option=value ...]")
        else:
            print(help_strings.HELP_MESSAGE)


    def do_list(self, _):
        """Lists the available CAN commands."""
        print(help_strings.COMMAND_LIST)


    def do_exit(self, _):
        """Exits the CLI."""
        return True


# ----------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------

def parse_send(args: str) -> tuple[bytes, str, dict, str]:
    """Parses arguments for `do_send`."""
    parts = args.split()

    cmd_id = parts[0]
    data = bytearray(DATA_SIZE)
    data_index = 0
    options = {}

    for index, part in enumerate(parts[1:]):
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

# ----------------------------------------------------------
# MAIN APPLICATION CODE
# ----------------------------------------------------------

# ascii art lol
# font taken from https://patorjk.com/software/taag/
SPLASH = """
_._*_   ________  __________ .__'_        _
___*   / __/ __ \\/_  __/  _/   __*'.     \\ \\_____
.___  _\\ \\/ /_/ / / / _/ /    '__*.   ###[==_____>
_'._ /___/\\____/ /_/ /___/   *_.__       /_/
"""


if __name__ == "__main__":
    try:
        print(SPLASH)
        print("\nWelcome to the SOTI CLI!\n")

        print("Available Input Sources:")

        virtual_port = serial.tools.list_ports_common.ListPortInfo("Virtual")
        virtual_port.description = "Run in virtual mode for off-board testing."

        sources = sorted(serial.tools.list_ports.comports()) + [virtual_port]

        for i, port in enumerate(sources):
            print(str(i) + ": " + port.device + " - " + port.description)
        print()

        # Prompt user for valid port.
        while True:
            try:
                source_number = int(input("Please choose an input source:"))
                selected_port = sources[source_number]
                break
            except (ValueError, IndexError):
                pass
            print("Invalid input. Please enter the number corresponding to your selection.")

        virtual_mode = selected_port is virtual_port

        multiprocessing.set_start_method('spawn')
        write_msg_queue = multiprocessing.Queue() # messages to be written to file
        out_msg_queue = multiprocessing.Queue() # messages to send to SOTI board

        # thread-safe flags to tell the processes to stop.
        stop_serial_reader_flag = multiprocessing.Event()
        stop_session_logger_flag = multiprocessing.Event()

        processes = []

        # create the serial handler process
        if not virtual_mode:
            processes.append(multiprocessing.Process(
                target=serial_reader,
                args=(
                    write_msg_queue,
                    out_msg_queue,
                    stop_serial_reader_flag,
                    selected_port.device
                    ),
                daemon=True)
            )

        # create the session logger process
        processes.append(multiprocessing.Process(
            target=log_messages,
            args=(
                write_msg_queue,
                stop_session_logger_flag,
                selected_port.device
            ),
            daemon=True)
        )

        # start the processes
        for p in processes:
            p.start()

        CommandLine(out_msg_queue, write_msg_queue).cmdloop()

    except KeyboardInterrupt:
        pass

    finally:
        # tell the processes to stop
        stop_serial_reader_flag.set()
        stop_session_logger_flag.set()

        for p in processes:
            p.join()

        print("\nExiting...")
