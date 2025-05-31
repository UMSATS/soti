"""Global constants used in the program."""

from enum import Enum, auto
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

SAVE_DATA_DIR = ROOT_DIR / "save-data"

SESSIONS_DIR = SAVE_DATA_DIR / "sessions"

RES_DIR = ROOT_DIR / "res"

# Used to name session files with datetime.strftime()
SESSION_FILE_FORMAT = "%Y-%m-%d_%H%M%S"

# The length of a serialized message in bytes.
MSG_SIZE = 11
# The length of a message's data payload in bytes.
DATA_SIZE = 7


class NodeID(Enum):
    """Associates a subsystem id with a human-readable name for message history."""
    CDH  = 0
    PWR  = 1
    ADCS = 2
    PLD  = 3

    def get_display_name(self) -> str:
        """
        Returns a friendlier name for each enum member.
        
        Example Usage:
        print(Node.CDH.get_display_name())
        """

        display_names = {
            NodeID.CDH: "CDH",
            NodeID.PWR: "Power",
            NodeID.ADCS: "ADCS",
            NodeID.PLD: "Payload"
        }
        return display_names[self]


class CmdID(Enum):
    """Command IDs copied from TSAT Utilities Kit's CmdID enum"""
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
    CmdID.COMM_RESET:                      {"priority": 0, "dest": None},
    CmdID.COMM_PREPARE_FOR_SHUTDOWN:       {"priority": 1, "dest": None},
    CmdID.COMM_GET_TELEMETRY:              {"priority": 32, "dest": None},
    CmdID.COMM_SET_TELEMETRY_INTERVAL:     {"priority": 32, "dest": None},
    CmdID.COMM_GET_TELEMETRY_INTERVAL:     {"priority": 32, "dest": None},
    CmdID.COMM_UPDATE_START:               {"priority": 32, "dest": None},
    CmdID.COMM_UPDATE_LOAD:                {"priority": 32, "dest": None},
    CmdID.COMM_UPDATE_END:                 {"priority": 32, "dest": None},

    ############################################
    ### CDH
    ############################################
    ## Event Processing.
    CmdID.CDH_PROCESS_HEARTBEAT:           {"priority": 2, "dest": NodeID.CDH},
    CmdID.CDH_PROCESS_RUNTIME_ERROR:       {"priority": 10, "dest": NodeID.CDH},
    CmdID.CDH_PROCESS_COMMAND_ERROR:       {"priority": 10, "dest": NodeID.CDH},
    CmdID.CDH_PROCESS_NOTIFICATION:        {"priority": 2, "dest": NodeID.CDH},
    CmdID.CDH_PROCESS_TELEMETRY_REPORT:    {"priority": 3, "dest": NodeID.CDH},
    CmdID.CDH_PROCESS_RETURN:              {"priority": 32, "dest": NodeID.CDH},
    CmdID.CDH_PROCESS_LED_TEST:            {"priority": 4, "dest": NodeID.CDH},

    ## Clock
    CmdID.CDH_SET_RTC:                     {"priority": 32, "dest": NodeID.CDH},
    CmdID.CDH_GET_RTC:                     {"priority": 32, "dest": NodeID.CDH},

    ## Tests
    CmdID.CDH_TEST_FLASH:                  {"priority": 32, "dest": NodeID.CDH},
    CmdID.CDH_TEST_MRAM:                   {"priority": 32, "dest": NodeID.CDH},

    CmdID.CDH_RESET_SUBSYSTEM:             {"priority": 32, "dest": NodeID.CDH},

    ## Antenna
    CmdID.CDH_ENABLE_ANTENNA:              {"priority": 32, "dest": NodeID.CDH},
    CmdID.CDH_DEPLOY_ANTENNA:              {"priority": 32, "dest": NodeID.CDH},

    ############################################
    ### POWER
    ############################################
    CmdID.PWR_PROCESS_HEARTBEAT:           {"priority": 2, "dest": NodeID.PWR},
    CmdID.PWR_SET_SUBSYSTEM_POWER:         {"priority": 0, "dest": NodeID.PWR},
    CmdID.PWR_GET_SUBSYSTEM_POWER:         {"priority": 32, "dest": NodeID.PWR},
    CmdID.PWR_SET_BATTERY_HEATER_POWER:    {"priority": 5, "dest": NodeID.PWR},
    CmdID.PWR_GET_BATTERY_HEATER_POWER:    {"priority": 32, "dest": NodeID.PWR},
    CmdID.PWR_SET_BATTERY_ACCESS:          {"priority": 32, "dest": NodeID.PWR},
    CmdID.PWR_GET_BATTERY_ACCESS:          {"priority": 32, "dest": NodeID.PWR},

    ############################################
    ### ADCS
    ############################################
    CmdID.ADCS_SET_MAGNETORQUER_DIRECTION: {"priority": 32, "dest": NodeID.ADCS},
    CmdID.ADCS_GET_MAGNETORQUER_DIRECTION: {"priority": 32, "dest": NodeID.ADCS},
    CmdID.ADCS_SET_OPERATING_MODE:         {"priority": 32, "dest": NodeID.ADCS},
    CmdID.ADCS_GET_OPERATING_MODE:         {"priority": 32, "dest": NodeID.ADCS},

    ############################################
    ### PAYLOAD
    ############################################
    CmdID.PLD_SET_ACTIVE_ENVS:             {"priority": 32, "dest": NodeID.PLD},
    CmdID.PLD_GET_ACTIVE_ENVS:             {"priority": 32, "dest": NodeID.PLD},
    CmdID.PLD_SET_SETPOINT:                {"priority": 32, "dest": NodeID.PLD},
    CmdID.PLD_GET_SETPOINT:                {"priority": 32, "dest": NodeID.PLD},
    CmdID.PLD_SET_TOLERANCE:               {"priority": 32, "dest": NodeID.PLD},
    CmdID.PLD_GET_TOLERANCE:               {"priority": 32, "dest": NodeID.PLD},
    CmdID.PLD_TEST_LEDS:                   {"priority": 4, "dest": NodeID.PLD}
}
