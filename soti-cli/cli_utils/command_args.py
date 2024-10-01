from constants import CmdID, NodeID
import struct


# Extracts an integer of any width from a bytes object
def extract_int(data: bytes, index: int, size: int, signed: bool = False) -> int:
    return int.from_bytes(data[index:(size+index)], byteorder='little', signed=signed)


# Extracts a 32-bit float from a bytes object
def extract_float(data: bytes, index: int) -> float:
    return struct.unpack('<f', data[index:(4+index)])[0]


# Returns a hexadecimal representation of the provided data
def to_hex_str(data: bytes) -> str:
    return "0x" + data.hex()


# Returns a binary representation of the provided data
def to_bin_str(data: bytes) -> str:
    bit_string = ''
    for byte in data:
        bits = bin(byte)[2:]  # remove '0b' prefix
        bit_string += bits.zfill(8)  # pad with zeros to 8 bits
    return "0b" + bit_string


# adds command args to the output json
def parse_msg_body(cmd_id: CmdID, body: bytes) -> dict:
    output = {}
    
    match cmd_id:
        
        # Common
        case CmdID.COMM_GET_TELEMETRY:
            output['telemetry-key'] = body[0]
        case CmdID.COMM_SET_TELEMETRY_INTERVAL:
            output['telemetry-key'] = body[0]
            output['interval'] = extract_int(body, 1, 2)
        case CmdID.COMM_GET_TELEMETRY_INTERVAL:
            output['telemetry-key'] = body[0]
        case CmdID.COMM_UPDATE_START:
            output['address'] = extract_int(body, 0, 4)
        case CmdID.COMM_UPDATE_LOAD:
            output['data'] = to_hex_str(body)
        
        # CDH
        case CmdID.CDH_PROCESS_RUNTIME_ERROR:
            output['error-code'] = body[0]
            output['context-code'] = body[1]
            output['debug-data'] = to_hex_str(body[2:7])
        case CmdID.CDH_PROCESS_COMMAND_ERROR:
            output['error-code'] = body[0]
            output['command-id'] = CmdID(body[1])
            output['debug-data'] = to_hex_str(body[2:7])
        case CmdID.CDH_PROCESS_NOTIFICATION:
            output['notification-id'] = body[0]
        case CmdID.CDH_PROCESS_TELEMETRY_REPORT:
            output['telemetry-key'] = body[0]
            output['sequence-number'] = body[1]
            output['packet-number'] = body[2]
            output['telemetry'] = to_hex_str(body[3:7])
        case CmdID.CDH_PROCESS_RETURN:
            output['command-id'] = CmdID(body[0])
            output['data'] = to_hex_str(body[1:7])
        case CmdID.CDH_PROCESS_LED_TEST:
            output['bitmap'] = to_bin_str(body[:2])
        case CmdID.CDH_SET_RTC:
            output['unix-timestamp'] = extract_int(body, 0, 4)
        case CmdID.CDH_RESET_SUBSYSTEM:
            output['subsystem-id'] = NodeID(body[0])
        
        # Power
        case CmdID.PWR_SET_SUBSYSTEM_POWER:
            output['subsystem-id'] = NodeID(body[0])
            output['power'] = bool(body[1])
        case CmdID.PWR_GET_SUBSYSTEM_POWER:
            output['subsystem-id'] = NodeID(body[0])
        case CmdID.PWR_SET_BATTERY_HEATER_POWER:
            output['heater-power'] = bool(body[0])
        case CmdID.PWR_SET_BATTERY_ACCESS:
            output['battery-access'] = bool(body[0])
        
        # ADCS
        case CmdID.ADCS_SET_MAGNETORQUER_DIRECTION:
            output['magnetorquer-id'] = body[0]
            output['direction'] = extract_int(body, 1, 1, signed=True)
        case CmdID.ADCS_GET_MAGNETORQUER_DIRECTION:
            output['magnetorquer-id'] = body[0]
        case CmdID.ADCS_SET_OPERATING_MODE:
            output['mode'] = body[0]
        
        # Payload
        case CmdID.PLD_SET_ACTIVE_ENVS:
            output['bitmap'] = to_bin_str(body[:2])
        case CmdID.PLD_GET_SETPOINT:
            output['well-id'] = body[0]
            output['setpoint'] = extract_float(body, 1)
        case CmdID.PLD_GET_SETPOINT:
            output['well-id'] = body[0]
        case CmdID.PLD_SET_TOLERANCE:
            output['tolerance'] = extract_float(body, 0)
    
    return output