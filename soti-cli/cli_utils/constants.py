from enum import Enum, auto

# files
MSG_HISTORY_FILENAME = "messages.json"

# message size
MSG_SIZE = 11

# associates a subsystem id with a human-readable name for message history
class NodeID(Enum):
    CDH     = 0
    Power   = 1
    ADCS    = 2
    Payload = 3

# command IDs copied from TSAT Utilities Kit's CmdID enum
class CmdID(Enum):
    ############################################
    ### COMMON
    ############################################
    COMM_RESET                      = 0
    COMM_PREPARE_FOR_SHUTDOWN       = auto()
    COMM_GET_TELEMETRY              = auto()
    COMM_SET_TELEMETRY_INTERVAL     = auto()
    COMM_GET_TELEMETRY_INTERVAL     = auto()
    COMM_UPDATE_START               = auto()
    COMM_UPDATE_LOAD                = auto()
    COMM_UPDATE_END                 = auto()

    ############################################
    ### CDH
    ############################################
    ## Event Processing.
    CDH_PROCESS_HEARTBEAT           = auto()
    CDH_PROCESS_RUNTIME_ERROR       = auto()
    CDH_PROCESS_COMMAND_ERROR       = auto()
    CDH_PROCESS_NOTIFICATION        = auto()
    CDH_PROCESS_TELEMETRY_REPORT    = auto()
    CDH_PROCESS_RETURN              = auto()
    CDH_PROCESS_LED_TEST            = auto()   

    ## Clock
    CDH_SET_RTC                     = auto()
    CDH_GET_RTC                     = auto()

    ## Tests
    CDH_TEST_FLASH                  = auto()
    CDH_TEST_MRAM                   = auto()

    CDH_RESET_SUBSYSTEM             = auto()

    ## Antenna
    CDH_ENABLE_ANTENNA              = auto()
    CDH_DEPLOY_ANTENNA              = auto()

    ############################################
    ### POWER
    ############################################
    PWR_PROCESS_HEARTBEAT           = auto()
    PWR_SET_SUBSYSTEM_POWER         = auto()
    PWR_GET_SUBSYSTEM_POWER         = auto()
    PWR_SET_BATTERY_HEATER_POWER    = auto()
    PWR_GET_BATTERY_HEATER_POWER    = auto()
    PWR_SET_BATTERY_ACCESS          = auto()
    PWR_GET_BATTERY_ACCESS          = auto()

    ############################################
    ### ADCS
    ############################################
    ADCS_SET_MAGNETORQUER_DIRECTION = auto()
    ADCS_GET_MAGNETORQUER_DIRECTION = auto()
    ADCS_SET_OPERATING_MODE         = auto()
    ADCS_GET_OPERATING_MODE         = auto()

    ############################################
    ### PAYLOAD
    ############################################
    PLD_SET_ACTIVE_ENVS             = auto()
    PLD_GET_ACTIVE_ENVS             = auto()
    PLD_SET_SETPOINT                = auto()
    PLD_GET_SETPOINT                = auto()
    PLD_SET_TOLERANCE               = auto()
    PLD_GET_TOLERANCE               = auto()
    PLD_TEST_LEDS                   = auto()

# constants for command codes & priorities
COMM_INFO = {
    ############################################
    ### COMMON
    ############################################
    CmdID.COMM_RESET.value:
    {"priority": 0, "dest": None},
    CmdID.COMM_PREPARE_FOR_SHUTDOWN.value:
    {"priority": 1, "dest": None},
    CmdID.COMM_GET_TELEMETRY.value:
    {"priority": 32, "dest": None},
    CmdID.COMM_SET_TELEMETRY_INTERVAL.value:
    {"priority": 32, "dest": None},
    CmdID.COMM_GET_TELEMETRY_INTERVAL.value: 
    {"priority": 32, "dest": None},
    CmdID.COMM_UPDATE_START.value: 
    {"priority": 32, "dest": None},
    CmdID.COMM_UPDATE_LOAD.value: 
    {"priority": 32, "dest": None},
    CmdID.COMM_UPDATE_END.value: 
    {"priority": 32, "dest": None},

    ############################################
    ### CDH
    ############################################
    ## Event Processing.
    CmdID.CDH_PROCESS_HEARTBEAT.value:
    {"priority": 2, "dest": NodeID.CDH.value},
    CmdID.CDH_PROCESS_RUNTIME_ERROR.value: 
    {"priority": 10, "dest": NodeID.CDH.value},
    CmdID.CDH_PROCESS_COMMAND_ERROR.value: 
    {"priority": 10, "dest": NodeID.CDH.value},
    CmdID.CDH_PROCESS_NOTIFICATION.value: 
    {"priority": 2, "dest": NodeID.CDH.value},
    CmdID.CDH_PROCESS_TELEMETRY_REPORT.value: 
    {"priority": 3, "dest": NodeID.CDH.value},
    CmdID.CDH_PROCESS_RETURN.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CDH_PROCESS_LED_TEST.value: 
    {"priority": 4, "dest": NodeID.CDH.value},

    ## Clock
    CmdID.CDH_SET_RTC.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CDH_GET_RTC.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    ## Tests
    CmdID.CDH_TEST_FLASH.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CDH_TEST_MRAM.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    CmdID.CDH_RESET_SUBSYSTEM.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    ## Antenna
    CmdID.CDH_ENABLE_ANTENNA.value: 
    {"priority": 32, "dest": NodeID.CDH.value},
    CmdID.CDH_DEPLOY_ANTENNA.value: 
    {"priority": 32, "dest": NodeID.CDH.value},

    ############################################
    ### POWER
    ############################################
    CmdID.PWR_PROCESS_HEARTBEAT.value: 
    {"priority": 2, "dest": NodeID.Power.value},
    CmdID.PWR_SET_SUBSYSTEM_POWER.value: 
    {"priority": 0, "dest": NodeID.Power.value},
    CmdID.PWR_GET_SUBSYSTEM_POWER.value: 
    {"priority": 32, "dest": NodeID.Power.value},
    CmdID.PWR_SET_BATTERY_HEATER_POWER.value: 
    {"priority": 5, "dest": NodeID.Power.value},
    CmdID.PWR_GET_BATTERY_HEATER_POWER.value: 
    {"priority": 32, "dest": NodeID.Power.value},
    CmdID.PWR_SET_BATTERY_ACCESS.value: 
    {"priority": 32, "dest": NodeID.Power.value},
    CmdID.PWR_GET_BATTERY_ACCESS.value: 
    {"priority": 32, "dest": NodeID.Power.value},

    ############################################
    ### ADCS
    ############################################
    CmdID.ADCS_SET_MAGNETORQUER_DIRECTION.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},
    CmdID.ADCS_GET_MAGNETORQUER_DIRECTION.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},
    CmdID.ADCS_SET_OPERATING_MODE.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},
    CmdID.ADCS_GET_OPERATING_MODE.value: 
    {"priority": 32, "dest": NodeID.ADCS.value},

    ############################################
    ### PAYLOAD
    ############################################
    CmdID.PLD_SET_ACTIVE_ENVS.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.PLD_GET_ACTIVE_ENVS.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.PLD_SET_SETPOINT.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.PLD_GET_SETPOINT.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.PLD_SET_TOLERANCE.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.PLD_GET_TOLERANCE.value: 
    {"priority": 32, "dest": NodeID.Payload.value},
    CmdID.PLD_TEST_LEDS.value: 
    {"priority": 4, "dest": NodeID.Payload.value}
}
# add command names using CmdID
for key in CmdID:
    COMM_INFO[key.value]['name'] = key.name
