import socket as sock

from threading import Thread
from queue import Queue
from bitstring import BitArray
import datetime
import os
import subprocess

GR_IP = "127.0.0.1"
GR_PORT = 2000

GR_ADDR = (GR_IP, GR_PORT)

# TODO: Does this effect performance? -NJR
GR_PACKET_SIZE = 1024

# Section 3.1
FLAG_SEQ = "0x7E"

# Section 3.10
ABORT_SEQ = "0b111111111111111"

POST_BITSTUFF_SEQ = "0b111110"
PRE_BITSTUFF_SEQ = "0b11111"

MIN_PACKET_SIZE = 17

BITS_PER_BYTE = 8

# 63 bytes less two flag bytes - NJR
MAX_PACKET_LEN = 61

VERSION = 0.1

SPLASH_SCREEN = f"""\
                Spacecraft Operations and Test Interface
                ------------------SOTI------------------

University of Manitoba Space Applications and Technology Society (UMSATS)

               AX.25 Packet Test Viewer Version {VERSION}

"""

data_queue = Queue()

"""
Adds a timestamp to data sent to stdout.
"""
def log(string: str) -> None:
    curr_time = datetime.datetime.now().strftime("%T")
    print(f"{curr_time}: {string}")

"""
Shift all bytes in the given array by n bits right.
"""
def shift_bytes(b: bytearray, n: int) -> bytearray:
    assert(n >= 0 and n <= 8)
    output = bytearray()

    for byte in b:
        output.append(byte >> n)

    return output

"""
Attempts to scrape the callsigns, SSIDs, and Info field from the packet.
"""
def parse_packet(packet_data: BitArray) -> None:
    # Everything but the flag fields are bitstuffed.
    # TODO: TEST THIS!!!!!!!!!!!!!! -NJR

    # Get rid of the flag.
    flag_stripped = packet_data[8:-8]

    flag_stripped.replace(POST_BITSTUFF_SEQ, PRE_BITSTUFF_SEQ)
    
    # Reverse the order of the bits to MSB First (I think??????) -NJR
    msb_first = flag_stripped
    for i in range(len(msb_first)):
        msb_first[8*i:8*i + 8] = msb_first[8*i:8*i + 8][::-1]

    decoded_bytes = bytearray(msb_first[:-16].tobytes())

    
    # CRC Bits: All ones to start, most significant bit first, Big-endian. (ISO-3309)
    # TODO: Actually do the CRC Check. There is a lot of Uncertainty with it online 
    # so figure it out later.
    if (len(decoded_bytes) < MIN_PACKET_SIZE):
        log("Invalid packet decoded!")
        return False
    
    elif (len(decoded_bytes) > BITS_PER_BYTE * MAX_PACKET_LEN):
        log("Packet too long, probably not valid.")
        return False

    else:
        try:
            to_call = str(shift_bytes(decoded_bytes[0:6], 1), "utf-8")
            to_ssid = str((int(decoded_bytes[6]) >> 1) & 0x0F)

            from_call = str(shift_bytes(decoded_bytes[7:13], 1), "utf-8")
            from_ssid = str((int(decoded_bytes[13]) >> 1) & 0x0F)

            control_bits = decoded_bytes[14]
            protocol_id = decoded_bytes[15]

            info_field = str(decoded_bytes[16:], "utf-8")

            log(f"Decoded Frame: {from_call}-{from_ssid}>{to_call}-{to_ssid}: {info_field}")
        except:
            log("Error: Packet unable to be decoded.")
            return False
    
    return True


"""
Continually read data from the shared FIFO and attempt to find a packet.
"""
def consume_data() -> None:
    packet_bits = BitArray()
    packet_data = BitArray()

    while (True):
        # Simply block until we get the data.
        new_data = BitArray(data_queue.get())

        # for i in range(len(new_data)):
        #     new_data[8*i:8*i + 8] = new_data[8*i:8*i + 8][::-1]


        packet_bits.append(new_data)

        # Look for a start and end. 
        if ((start_pos := packet_bits.find(FLAG_SEQ))):
            # and not packet_bits.find(ABORT_SEQ, start=start_pos[0])):

            # We need to flip the order of the bits 

            print("Start found!")
            # BitArray.find() produces a tuple (to allow for boolean )
            if (end_pos := packet_bits.find(FLAG_SEQ, start=(start_pos[0]+8))):
                
                print("End Found!")

                packet_data = packet_bits[start_pos[0]:end_pos[0]+8]
                packet_bits = packet_bits[end_pos[0]+8:]

                if (parse_packet(packet_data)):
                    log(f"Packet found: {str(packet_data.tobytes())}")
            elif (packet_bits.find(ABORT_SEQ, start=start_pos[0])):
                log(f"Abort sequence found, likely no packet. Clearing buffer.")
                packet_bits.clear()
        else:
            # The flag might not be fully here yet,
            # so get rid of everything but the last <8 bits.
            packet_bits = packet_bits[-7:]

"""
Continually feed the FIFO with data received over the given port.
"""
def main():
    print(SPLASH_SCREEN)

    print(f"Starting GNURadio...")

    subprocess.Popen(["python3", "./fft.py"])

    print(f"Attempting to connect to {GR_ADDR}... ", end="")

    # UDP
    with sock.socket(sock.AF_INET, sock.SOCK_DGRAM) as input_socket:
        print(f"Connected.")
        input_socket.bind(GR_ADDR)

        parser_thread = Thread(target=consume_data)
        parser_thread.start()

        while(True):
            received_bytes, _ = input_socket.recvfrom(GR_PACKET_SIZE)
            data_queue.put(received_bytes)


if (__name__ == "__main__"):
    main()
