from enum import Enum, auto

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
class CmdID(Enum):
    ############################################
    ### COMMON
    ############################################
    CMD_COMM_RESET                      = 0
    CMD_COMM_PREPARE_FOR_SHUTDOWN       = auto()
    CMD_COMM_GET_TELEMETRY              = auto()
    CMD_COMM_SET_TELEMETRY_INTERVAL     = auto()
    CMD_COMM_GET_TELEMETRY_INTERVAL     = auto()
    CMD_COMM_UPDATE_START               = auto()
    CMD_COMM_UPDATE_LOAD                = auto()
    CMD_COMM_UPDATE_END                 = auto()

    ############################################
    ### CDH
    ############################################
    ## Event Processing.
    CMD_CDH_PROCESS_HEARTBEAT           = auto()
    CMD_CDH_PROCESS_RUNTIME_ERROR       = auto()
    CMD_CDH_PROCESS_COMMAND_ERROR       = auto()
    CMD_CDH_PROCESS_NOTIFICATION        = auto()
    CMD_CDH_PROCESS_TELEMETRY_REPORT    = auto()
    CMD_CDH_PROCESS_RETURN              = auto()
    CMD_CDH_PROCESS_LED_TEST            = auto()   

    ## Clock
    CMD_CDH_SET_RTC                     = auto()
    CMD_CDH_GET_RTC                     = auto()

    ## Tests
    CMD_CDH_TEST_FLASH                  = auto()
    CMD_CDH_TEST_MRAM                   = auto()

    CMD_CDH_RESET_SUBSYSTEM             = auto()

    ## Antenna
    CMD_CDH_ENABLE_ANTENNA              = auto()
    CMD_CDH_DEPLOY_ANTENNA              = auto()

    ############################################
    ### POWER
    ############################################
    CMD_PWR_PROCESS_HEARTBEAT           = auto()
    CMD_PWR_SET_SUBSYSTEM_POWER         = auto()
    CMD_PWR_GET_SUBSYSTEM_POWER         = auto()
    CMD_PWR_SET_BATTERY_HEATER_POWER    = auto()
    CMD_PWR_GET_BATTERY_HEATER_POWER    = auto()
    CMD_PWR_SET_BATTERY_ACCESS          = auto()
    CMD_PWR_GET_BATTERY_ACCESS          = auto()

    ############################################
    ### ADCS
    ############################################
    CMD_ADCS_SET_MAGNETORQUER_DIRECTION = auto()
    CMD_ADCS_GET_MAGNETORQUER_DIRECTION = auto()
    CMD_ADCS_SET_OPERATING_MODE         = auto()
    CMD_ADCS_GET_OPERATING_MODE         = auto()

    ############################################
    ### PAYLOAD
    ############################################
    CMD_PLD_SET_ACTIVE_ENVS             = auto()
    CMD_PLD_GET_ACTIVE_ENVS             = auto()
    CMD_PLD_SET_SETPOINT                = auto()
    CMD_PLD_GET_SETPOINT                = auto()
    CMD_PLD_SET_TOLERANCE               = auto()
    CMD_PLD_GET_TOLERANCE               = auto()
    CMD_PLD_TEST_LEDS                   = auto()

# constants for command codes & priorities
COMM_INFO = {
    ############################################
    ### COMMON
    ############################################
    CmdID.CMD_COMM_RESET.value:
    {"priority": 0, "dest": None},
    CmdID.CMD_COMM_PREPARE_FOR_SHUTDOWN.value:
    {"priority": 1, "dest": None},
    CmdID.CMD_COMM_GET_TELEMETRY.value:
    {"priority": 32, "dest": None},
    CmdID.CMD_COMM_SET_TELEMETRY_INTERVAL.value:
    {"priority": 32, "dest": None},
    CmdID.CMD_COMM_GET_TELEMETRY_INTERVAL.value: 
    {"priority": 32, "dest": None},
    CmdID.CMD_COMM_UPDATE_START.value: 
    {"priority": 32, "dest": None},
    CmdID.CMD_COMM_UPDATE_LOAD.value: 
    {"priority": 32, "dest": None},
    CmdID.CMD_COMM_UPDATE_END.value: 
    {"priority": 32, "dest": None},

    ############################################
    ### CDH
    ############################################
    ## Event Processing.
    CmdID.CMD_CDH_PROCESS_HEARTBEAT.value:
    {"priority": 2, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_PROCESS_RUNTIME_ERROR.value: 
    {"priority": 10, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_PROCESS_COMMAND_ERROR.value: 
    {"priority": 10, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_PROCESS_NOTIFICATION.value: 
    {"priority": 2, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_PROCESS_TELEMETRY_REPORT.value: 
    {"priority": 3, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_PROCESS_RETURN.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_PROCESS_LED_TEST.value: 
    {"priority": 4, "dest": NodeID.CDH.value},

    ## Clock
    CmdID.CMD_CDH_SET_RTC.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_GET_RTC.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    ## Tests
    CmdID.CMD_CDH_TEST_FLASH.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_TEST_MRAM.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    CmdID.CMD_CDH_RESET_SUBSYSTEM.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    ## Antenna
    CmdID.CMD_CDH_ENABLE_ANTENNA.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CMD_CDH_DEPLOY_ANTENNA.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    ############################################
    ### POWER
    ############################################
    CmdID.CMD_PWR_PROCESS_HEARTBEAT.value: 
    {"priority": 2, "dest": NodeID.Power.value},
    CmdID.CMD_PWR_SET_SUBSYSTEM_POWER.value: 
    {"priority": 0, "dest": NodeID.Power.value},
    CmdID.CMD_PWR_GET_SUBSYSTEM_POWER.value: 
    {"priority": 32, "dest": NodeID.Power.value},
    CmdID.CMD_PWR_SET_BATTERY_HEATER_POWER.value: 
    {"priority": 5, "dest": NodeID.Power.value},
    CmdID.CMD_PWR_GET_BATTERY_HEATER_POWER.value: 
    {"priority": 32, "dest": NodeID.Power.value},
    CmdID.CMD_PWR_SET_BATTERY_ACCESS.value: 
    {"priority": 32, "dest": NodeID.Power.value},
    CmdID.CMD_PWR_GET_BATTERY_ACCESS.value: 
    {"priority": 32, "dest": NodeID.Power.value},

    ############################################
    ### ADCS
    ############################################
    CmdID.CMD_ADCS_SET_MAGNETORQUER_DIRECTION.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},
    CmdID.CMD_ADCS_GET_MAGNETORQUER_DIRECTION.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},
    CmdID.CMD_ADCS_SET_OPERATING_MODE.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},
    CmdID.CMD_ADCS_GET_OPERATING_MODE.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},

    ############################################
    ### PAYLOAD
    ############################################
    CmdID.CMD_PLD_SET_ACTIVE_ENVS.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.CMD_PLD_GET_ACTIVE_ENVS.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.CMD_PLD_SET_SETPOINT.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.CMD_PLD_GET_SETPOINT.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.CMD_PLD_SET_TOLERANCE.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.CMD_PLD_GET_TOLERANCE.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.CMD_PLD_TEST_LEDS.value: 
    {"priority": 4, "dest": NodeID.Payload.value}
}
# add command names using CmdID
for key in CmdID:
    COMM_INFO[key.value]['name'] = key.name
