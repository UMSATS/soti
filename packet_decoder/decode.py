import socket as sock

from threading import Thread
from queue import Queue
from bitstring import BitArray
import datetime

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

data_queue = Queue()

def log(string: str) -> None:
    curr_time = datetime.datetime.now().strftime("%T")
    print(f"{curr_time}: {string}")

"""
Reverse the order of bits in each byte of a bytearray, preserving endianness.
"""
def reverse_bits(b: bytes) -> bytes:
    output = b""

    for byte in b:
        output.append((BitArray(byte)[::-1]).tobytes())

    return output

"""
Shift all bytes in the given array by n bits right.
"""
def shift_bytes(b: bytes, n: int) -> bytes:
    assert(n >= 0 and n <= 8)
    output = b""

    for byte in b:
        output.append(byte >> n)

    return output

def parse_packet(packet_bits: BitArray) -> None:
    # Everything but the flag fields are bitstuffed.
    # TODO: TEST THIS!!!!!!!!!!!!!! -NJR
    decoded_data = packet_bits[8:-8].replace(POST_BITSTUFF_SEQ,
                                             PRE_BITSTUFF_SEQ)
    
    # TODO: Reverse bit order?
    decoded_bytes = packet_bits[8:-24].tobytes()
    
    # CRC Bits: All ones to start, most significant bit first, Big-endian. (ISO-3309)
    # TODO: Actually do the CRC Check. There is a lot of Uncertainty with it online 
    # so figure it out later.
    if (len(decoded_data) < 136 
        or len(decoded_data) % 8 != 0):
        log("Invalid packet decoded!")
    else:
        to_call = reverse_bits(shift_bytes(decoded_bytes[0:6]))
        to_ssid = (decoded_bytes[6:7] >> 1) & 0x0F

        from_call = reverse_bits(shift_bytes(decoded_bytes[7:13]))
        from_ssid = (decoded_bytes[13:14] >> 1) & 0x0F

        control_bits = decoded_bytes[14]
        protocol_id = decoded_bytes[15]

        info_field = reverse_bits(decoded_bytes[16:])

        log(f"Decoded Frame: {to_call}-{to_ssid}>{from_call}-{from_ssid}: {info_field}")

def consume_data() -> None:
    packet_bits = BitArray()
    packet_data = BitArray()

    while (True):
        # Simply block until we get the data.
        new_data = data_queue.get()
        packet_bits.append(new_data)

        # Look for a start and end. 
        if (start_pos := packet_bits.find(FLAG_SEQ)):
            # BitArray.find() produces a tuple (to allow for boolean )
            if (end_pos := packet_bits.find(FLAG_SEQ, start=(start_pos[0]+8)) 
                and not packet_bits.find(ABORT_SEQ, start=(start_pos[0]+8))):
                packet_data = packet_bits[start_pos[0]:end_pos[0]+8]
                packet_bits = packet_bits[end_pos[0]+8:]

                parse_packet(packet_data)
                
                print(f"{curr_time} Packet found: {str(packet_data.tobytes())}")
        else:
            # The flag might not be fully here yet,
            # so get rid of everything but the last <8 bits.
            packet_bits = packet_bits[-7:]



def main():
    # UDP
    with sock.socket(sock.AF_INET, sock.SOCK_DGRAM) as input_socket:
        input_socket.bind(GR_ADDR)

        parser_thread = Thread(target=consume_data)
        parser_thread.start()

        while(True):
            received_bytes, _ = input_socket.recvfrom(GR_PACKET_SIZE)
            data_queue.put(received_bytes)


if (__name__ == "__main__"):
    main()
