# SOTI CLI User Guide

## Prerequisites
Please install Python 3.8.6 or later. For the CLI to work correctly, the command `python3` or `python` must allow you to run Python3 scripts.

Please install the module [PySerial](https://pyserial.readthedocs.io/en/latest/index.html).

`pip install serial`

More detailed installation instructions [here](https://github.com/pyserial/pyserial#installation).

## How to run
To run the program, run `python3 .\soti.py` or `python .\soti.py`.

No arguments are required.

## Linux & MacOS instructions
Accessing the serial port is sometimes restricted to the super user.

Therefore, to run the program, run `sudo python3 .\soti.py` or `sudo python .\soti.py`.

## Specify port
The CLI will prompt you to enter a serial port to read to and write from.

**Please write this correctly, or the CLI will throw an exception!**

The SOTI terminal will present a list of your available ports:

`Windows ex. "COM6 - STMicroelectronics STLink Virtual COM Port (COM6)"`
`Linux ex. "/dev/ttyACM0 - STM32 STLink - ST-Link VCP Ctrl"`

From this list, find the port corresponding to your device.

Enter only the device name.

`Windows ex. Input "COM6" (without the quotation marks)`
`Linux ex. Input "/dev/ttyACM0" (without the quotation marks)`

## Send commands
To send a command, please use its command code, prefixed with "0x" and followed by any arguments in hexadecimal notation.

`>> send 0xB0`

`>> send 0xA101`

## Query for telemetry data
Telemetry messages are logged in the file `messages.json`.

`>> query battery-charge`

`>> query rotation-vector-1`