"""Global constants used in the program."""

from enum import Enum, auto
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

SAVE_DATA_DIR = ROOT_DIR / "save-data"

SESSIONS_DIR = SAVE_DATA_DIR / "sessions"

RES_DIR = ROOT_DIR / "res"

# Used to name session files with datetime.strftime()
SESSION_FILE_FORMAT = "%Y-%m-%d_%H%M%S"

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
