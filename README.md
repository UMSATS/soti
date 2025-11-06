# SOTI
Contains software for the SOTI (Satellite Operations Testing Interface) application, which runs on a NUCLEO-L452 development board.

## Overview
SOTI will be used to perform hardware-in-the-loop (HIL) testing with the TSAT6 satellite. HIL testing will be accomplished by connecting the NUCLEO development board to a CAN transceiver which is connected to the satellite's CAN bus. SOTI will provide a user-friendly terminal interface to make the HIL testing more efficient.

## Requirements
SOTI shall:
- Be able to send any custom CAN message.
- Sniff and log every CAN message which is transmitted over the CAN bus. These messages shall be time-stamped and written to a text file in chronological order.
- Parse the telemetry data from the sniffed CAN messages and write the data to individual text files.
- Be able to run custom testing scripts. The testing scripts shall be for individual systems, or for the entire satellite.

## Installation
SOTI is published on the Python Package Index (PyPI), so using it on your computer is just two steps.

### Install uv
First you need to install uv, which is a package manager for Python. If you use a package manager like Homebrew (macOS), winget (Windows), or your Linux distribution's package manager, use that to install uv. Further instructions are available in [uv's documentation](https://docs.astral.sh/uv/getting-started/installation/). If you don't use a package manager, here are some instructions for installing it directly.

On Linux or macOS, run this:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows, here is a PowerShell command (make sure you use PowerShell, not cmd.exe):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Make sure uv is available by running `uv --version`. You should get output that looks something like this:

```sh
uv 0.9.5 (Homebrew 2025-10-21)
```

### Install SOTI
Finally, you can install SOTI using the following command:

```sh
uv tool install 'git+https://github.com/UMSATS/soti@main#subdirectory=soti'

# now you can run SOTI like this:
soti
```

Alternately, if you just want to run SOTI once, use this command. It will download everything you need and run automatically:

```sh
uvx --from 'git+https://github.com/UMSATS/soti@main#subdirectory=soti' soti
```

### Update SOTI
To update, use uv's builtin updater.

```sh
uv tool upgrade umsats_soti
```

## Development
We use the uv package manager to develop SOTI. Instructions for installing uv are above.

Once uv is installed, you can run SOTI for development like this:

```
cd soti # enter soti subdirectory
uv run soti
```

uv will automatically install the correct Python version and all the dependencies.

## About UMSATS
UMSATS is a student driven group that works to build 3U nanosatellites to compete in the Canadian Satellite Design Challenge (CSDC).

Our website can be found here: http://www.umsats.ca/
