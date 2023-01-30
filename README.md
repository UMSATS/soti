# soti
Contains software for the SOTI (Satellite Operations Testing Interface) application, which runs on a NUCLEO-L452 development board.

## Overview
SOTI will be used to perform hardware-in-the-loop (HIL) testing with the TSAT6 satellite. HIL testing will be accomplished by connecting the NUCLEO development board to a CAN transceiver which is connected to the satellite's CAN bus. SOTI will provide a user-friendly terminal interface to make the HIL testing more efficient.

## Requirements
SOTI shall:
- Be able to send any custom CAN message.
- Sniff and log every CAN message which is transmitted over the CAN bus. These messages shall be time-stamped and written to a text file in chronological order.
- Parse the telemetry data from the sniffed CAN messages and write the data to individual text files.
- Be able to run custom testing scripts. The testing scripts shall be for individual systems, or for the entire satellite.

## About UMSATS
UMSATS is a student driven group that works to build 3U nanosatellites to compete in the Canadian Satellite Design Challenge (CSDC).

Our website can be found here: http://www.umsats.ca/
