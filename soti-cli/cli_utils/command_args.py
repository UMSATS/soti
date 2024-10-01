from cli_utils.constants import CmdID

# adds command args to the output json
def parse_args(args, output):
    data = Data(args)
    code = data.bytes(0)
    try:
        match CmdID(code):
            # Common
            case CmdID.COMM_GET_TELEMETRY:
                output['telemetry-key'] = data.bytes(1)
            case CmdID.COMM_SET_TELEMETRY_INTERVAL:
                output['telemetry-key'] = data.bytes(1)
                output['interval'] = data.bytes(2, 3)
            case CmdID.COMM_GET_TELEMETRY_INTERVAL:
                output['telemetry-key'] = data.bytes(1)
            case CmdID.COMM_UPDATE_START:
                output['address'] = data.bytes(1, 4)
            case CmdID.COMM_UPDATE_LOAD:
                output['data'] = data.bytes(1, 7)

            # CDH
            case CmdID.CDH_PROCESS_RUNTIME_ERROR:
                output['error-code'] = data.bytes(1)
                output['context-code'] = data.bytes(2)
                output['debug-data'] = data.bytes(3, 7)
            case CmdID.CDH_PROCESS_COMMAND_ERROR:
                output['error-code'] = data.bytes(1)
                output['command-id'] = data.bytes(2)
                output['debug-data'] = data.bytes(3, 7)
            case CmdID.CDH_PROCESS_NOTIFICATION:
                output['notification-id'] = data.bytes(1)
            case CmdID.CDH_PROCESS_TELEMETRY_REPORT:
                output['telemetry-key'] = data.bytes(1)
                output['sequence-number'] = data.bytes(2)
                output['packet-number'] = data.bytes(3)
                output['telemetry'] = data.bytes(4, 7)
            case CmdID.CDH_PROCESS_RETURN:
                output['command-id'] = data.bytes(1)
                output['data'] = data.bytes(2, 7)
            case CmdID.CDH_PROCESS_LED_TEST:
                output['bitmap'] = data.bytes(1, 2)
            case CmdID.CDH_SET_RTC:
                output['unix-timestamp'] = data.bytes(1, 4)
            case CmdID.CDH_RESET_SUBSYSTEM:
                output['subsystem-id'] = data.bytes(1)

            # Power
            case CmdID.PWR_SET_SUBSYSTEM_POWER:
                output['subsystem-id'] = data.bytes(1)
                output['power'] = data.bytes(2)
            case CmdID.PWR_GET_SUBSYSTEM_POWER:
                output['subsystem-id'] = data.bytes(1)
            case CmdID.PWR_SET_BATTERY_HEATER_POWER:
                output['heater-power'] = data.bytes(1)
            case CmdID.PWR_SET_BATTERY_ACCESS:
                output['battery-access'] = data.bytes(1)

            # ADCS
            case CmdID.ADCS_SET_MAGNETORQUER_DIRECTION:
                output['magnetorquer-id'] = data.bytes(1)
                output['direction'] = data.bytes(2)
            case CmdID.ADCS_GET_MAGNETORQUER_DIRECTION:
                output['magnetorquer-id'] = data.bytes(1)
            case CmdID.ADCS_SET_OPERATING_MODE:
                output['mode'] = data.bytes(1)

            # Payload
            case CmdID.PLD_SET_ACTIVE_ENVS:
                output['bitmap'] = data.bytes(1, 2)
            case CmdID.PLD_GET_SETPOINT:
                output['well-id'] = data.bytes(1)
                output['setpoint'] = data.bytes(2, 5)
            case CmdID.PLD_GET_SETPOINT:
                output['well-id'] = data.bytes(1)
            case CmdID.PLD_SET_TOLERANCE:
                output['tolerance'] = data.bytes(1, 4)
    
    except ValueError:
        pass

    return output

# use to extract bytes from a hex string
class Data:
    def __init__(self, args):
        self.data = bytearray.fromhex(args)

    # returns an int of the specified bytes (inclusive, big-endian)
    def bytes(self, start, end=None):
        if end is None:
            return self.data[start]
        else:
            return int.from_bytes(self.data[start:end+1])
