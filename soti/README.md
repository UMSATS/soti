# SOTI CLI User Guide

## Prerequisites

### Python 3.10

You will need Python 3.10 or later. To check which version you have, enter:

```
python3 --version
```

If your Python version is too old, install the latest version from [python.org](https://www.python.org/downloads/).

### Dependencies

Next, install the module [PySerial](https://pyserial.readthedocs.io/en/latest/index.html).

`pip install serial` & `pip install pyserial`

More detailed installation instructions [here](https://github.com/pyserial/pyserial#installation).

### Hardware

As of writing, the CLI program does not work without an STM32 board. Consider purchasing a [Nucleo-64](https://www.st.com/en/evaluation-tools/nucleo-l452re.html) or using the SOTI board found in the UMSATS lounge.

## How to run

First, plug in your board with a USB-B Micro cable.

To run the program, open the root folder in your terminal. Then run:

```
python3 soti
```

## Linux & MacOS instructions
Accessing the serial port is sometimes restricted to the super user.

Therefore, to run the program, run `sudo python3 soti`.

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
