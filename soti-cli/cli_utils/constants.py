from enum import Enum

# files
MSG_HISTORY_FILENAME = "messages.json"

# message size
MSG_SIZE = 11

# associates a subsystem id with a human-readable name for message history
class NodeID(Enum):
    CDH     = 0x0
    Power   = 0x1
    ADCS    = 0x2
    Payload = 0x3

# command IDs copied from TSAT Utilities Kit's CmdID enum
NUM_COMMANDS = 40
class CmdID(Enum): (
    ############################################
	### COMMON
	############################################
	CMD_COMM_RESET,
	CMD_COMM_PREPARE_FOR_SHUTDOWN,
	CMD_COMM_GET_TELEMETRY,
	CMD_COMM_SET_TELEMETRY_INTERVAL,
	CMD_COMM_GET_TELEMETRY_INTERVAL,
	CMD_COMM_UPDATE_START,
	CMD_COMM_UPDATE_LOAD,
	CMD_COMM_UPDATE_END,

	############################################
	### CDH
	############################################
	## Event Processing.
	CMD_CDH_PROCESS_HEARTBEAT,
	CMD_CDH_PROCESS_RUNTIME_ERROR,
	CMD_CDH_PROCESS_COMMAND_ERROR,
	CMD_CDH_PROCESS_NOTIFICATION,
	CMD_CDH_PROCESS_TELEMETRY_REPORT,
	CMD_CDH_PROCESS_RETURN,
	CMD_CDH_PROCESS_LED_TEST,

	## Clock
	CMD_CDH_SET_RTC,
	CMD_CDH_GET_RTC,

	## Tests
	CMD_CDH_TEST_FLASH,
	CMD_CDH_TEST_MRAM,

	CMD_CDH_RESET_SUBSYSTEM,

	## Antenna
	CMD_CDH_ENABLE_ANTENNA,
	CMD_CDH_DEPLOY_ANTENNA,

	############################################
	### POWER
	############################################
	CMD_PWR_PROCESS_HEARTBEAT,
	CMD_PWR_SET_SUBSYSTEM_POWER,
	CMD_PWR_GET_SUBSYSTEM_POWER,
	CMD_PWR_SET_BATTERY_HEATER_POWER,
	CMD_PWR_GET_BATTERY_HEATER_POWER,
	CMD_PWR_SET_BATTERY_ACCESS,
	CMD_PWR_GET_BATTERY_ACCESS,

	############################################
	### ADCS
	############################################
	CMD_ADCS_SET_MAGNETORQUER_DIRECTION,
	CMD_ADCS_GET_MAGNETORQUER_DIRECTION,
	CMD_ADCS_SET_OPERATING_MODE,
	CMD_ADCS_GET_OPERATING_MODE,

	############################################
	### PAYLOAD
	############################################
	CMD_PLD_SET_ACTIVE_ENVS,
	CMD_PLD_GET_ACTIVE_ENVS,
	CMD_PLD_SET_SETPOINT,
	CMD_PLD_GET_SETPOINT,
	CMD_PLD_SET_TOLERANCE,
	CMD_PLD_GET_TOLERANCE,
	CMD_PLD_TEST_LEDS
) = range(NUM_COMMANDS)

# constants for command codes & priorities
COMM_INFO = {
    # common commands
    0x01: {"priority": None, "dest": None, "name": "ack"},         # ack - priority depends on argument
    0x02: {"priority": None, "dest": None, "name": "nack"},         # nack - priority depends on argument
    0x10: {"priority": 0b0000000, "dest": 0x07, "name": "shutdown"},    # shutdown

    # CDH commands
    0x20: {"priority": 0b0000001, "dest": NodeID.CDH.value, "name": "heartbeat"},
    0x30: {"priority": 0b0000001, "dest": NodeID.CDH.value, "name": "process battery charge"},
    0x31: {"priority": 0b0000001, "dest": NodeID.CDH.value, "name": "process battery temperature"},
    0x32: {"priority": 0b0000001, "dest": NodeID.CDH.value, "name": "process satellite current consumption"},
    0x33: {"priority": 0b0011111, "dest": NodeID.CDH.value, "name": "process algae well light level"},
    0x34: {"priority": 0b0000011, "dest": NodeID.CDH.value, "name": "process algae well temperature"},
    0x35: {"priority": 0b0011111, "dest": NodeID.CDH.value, "name": "process rotation vector 1"},
    0x36: {"priority": 0b0011111, "dest": NodeID.CDH.value, "name": "process rotation vector 2"},
    0x40: {"priority": 0b0000000, "dest": NodeID.CDH.value, "name": "STM32 reset (CDH)"},
    0x41: {"priority": 0b0111111, "dest": NodeID.CDH.value, "name": "flash storage unit test"},
    0x42: {"priority": 0b0111111, "dest": NodeID.CDH.value, "name": "mram unit test"},
    0x43: {"priority": 0b0000000, "dest": NodeID.CDH.value, "name": "antenna deploy 1"},
    0x44: {"priority": 0b0000000, "dest": NodeID.CDH.value, "name": "antenna deploy 2"},
    0x46: {"priority": 0b0000111, "dest": NodeID.CDH.value, "name": "send UHF beacon"},
    0x47: {"priority": 0b0000111, "dest": NodeID.CDH.value, "name": "get CDH task list"},
    0x48: {"priority": 0b0000111, "dest": NodeID.CDH.value, "name": "sample time-tagged task"},
    0x49: {"priority": 0b0000111, "dest": NodeID.CDH.value, "name": "set internal rtc"},
    0x4A: {"priority": 0b0111111, "dest": NodeID.CDH.value, "name": "get internal rtc"},
    0x50: {"priority": 0b0000000, "dest": NodeID.CDH.value, "name": "PLD error report"},
    0x51: {"priority": 0b0000000, "dest": NodeID.CDH.value, "name": "ADCS error report"},
    0x52: {"priority": 0b0000000, "dest": NodeID.CDH.value, "name": "PWR error report"},

    # PLD commands
    0xA0: {"priority": 0b0000000, "dest": NodeID.Payload.value, "name": "STM32 reset (PLD)"},
    0xA1: {"priority": 0b0001111, "dest": NodeID.Payload.value, "name": "LED on"},
    0xA2: {"priority": 0b0000111, "dest": NodeID.Payload.value, "name": "LED off"},
    0xA3: {"priority": 0b0000011, "dest": NodeID.Payload.value, "name": "thermoregulation on"},
    0xA4: {"priority": 0b0000001, "dest": NodeID.Payload.value, "name": "thermoregulation off"},
    0xA5: {"priority": 0b0000011, "dest": NodeID.Payload.value, "name": "heater on"},
    0xA6: {"priority": 0b0000001, "dest": NodeID.Payload.value, "name": "heater off"},

    # ACDS commands
    0xB0: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "STM32 reset (ACDS)"},
    0xB1: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 1 full strength"},
    0xB2: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 2 full strength"},
    0xB3: {"priority": 0b0000111, "dest": NodeID.ADCS.value, "name": "magnetorquer 3 full strength"},
    0xB4: {"priority": 0b0000111, "dest": NodeID.ADCS.value, "name": "magnetorquer 1 off"},
    0xB5: {"priority": 0b0000111, "dest": NodeID.ADCS.value, "name": "magnetorquer 2 off"},
    0xB6: {"priority": 0b0000111, "dest": NodeID.ADCS.value, "name": "magnetorquer 3 off"},
    0xB7: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 1 forward"},
    0xB8: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 2 forward"},
    0xB9: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 3 forward"},
    0xBA: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 1 reverse"},
    0xBB: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 2 reverse"},
    0xBC: {"priority": 0b0001111, "dest": NodeID.ADCS.value, "name": "magnetorquer 3 reverse"},

    # PWR commands
    0xC0: {"priority": 0b0000000, "dest": NodeID.Power.value, "name": "STM32 reet (PWR)"},
    0xC1: {"priority": 0b0000001, "dest": NodeID.Power.value, "name": "PLD on"},
    0xC2: {"priority": 0b0000000, "dest": NodeID.Power.value, "name": "PLD off"},
    0xC3: {"priority": 0b0000001, "dest": NodeID.Power.value, "name": "ACDS on"},
    0xC4: {"priority": 0b0000000, "dest": NodeID.Power.value, "name": "ACDS off"},
    0xC5: {"priority": 0b0000011, "dest": NodeID.Power.value, "name": "battery access on"},
    0xC6: {"priority": 0b0000001, "dest": NodeID.Power.value, "name": "battery access off"},
    0xC7: {"priority": 0b0000011, "dest": NodeID.Power.value, "name": "battery heater on"},
    0xC8: {"priority": 0b0000001, "dest": NodeID.Power.value, "name": "battery heater off"},
    0xC9: {"priority": 0b0000111, "dest": NodeID.Power.value, "name": "check 3.3V DC-DC converter status"},
}

# associates the "query" attributes with their command code
# so they can be pulled out of the message history file
QUERY_ATTRS = {
    0x01: "ack",
    0x30: "battery-charge",
    0x31: "battery-temperature",
    0x32: "satellite-current-consumption",
    0x33: "algae-well-light-level",
    0x34: "algae-well-temperature",
    0x35: "rotation-vector-1",
    0x36: "rotation-vector-2",
}
