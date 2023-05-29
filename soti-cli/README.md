# SOTI CLI User Guide

## Prerequisites
Please install Python 3.8.6 or later. For the CLI to work correctly, the command `python3` must allow you to run Python scripts.

To verify this, try running:

`python3 cli.py`

It should throw an exception, but the important part is that it tries to run the script!

Please install the module [PySerial](https://pyserial.readthedocs.io/en/latest/index.html).

`pip install serial`

More detailed installation instructions [here](https://github.com/pyserial/pyserial#installation).

## Build and run
To build the executable, run `make`.

Then, run it with:

`cli`

or

`./cli`

 No arguments are required.

## Specify port
The CLI will prompt you to enter a serial port to read to and write from.

**Please write this correctly, or the CLI will throw an exception!**

Once you've installed PySerial, you can see a list of your available ports with the command:

`python -m serial.tools.list_ports`

From this list, find the port corresponding to your device.

## Send commands
To send a command, please use its command code, prefixed with "0x" and followed by any arguments in hexadecimal notation.

`> send 0xB0`

`> send 0xA101`

## Query for telemetry data
Telemetry messages are logged in the file `messages.json`. Use `-h` with the `query` command to see which attributes you can search for.

`query battery-charge`

`query rotation-vector-1`