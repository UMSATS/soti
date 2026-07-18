/** (c) 2024 UMSATS
 * @file can_command_list.c
 *
 * Configurations for all valid command ID's.
 */

#include "tuk/can_wrapper/can_command_list.h"

const CmdConfig CMD_CONFIGS[NUM_COMMANDS] = {
		////////////////////////////////////////////
		/// COMMON
		////////////////////////////////////////////
		//CMD                                 //BODY SIZE //PRIORITY
		[CMD_COMM_RESET]                       ={0, 0 },
		[CMD_COMM_PREPARE_FOR_SHUTDOWN]        ={0, 1 },
		[CMD_COMM_GET_TELEMETRY]               ={1, 32},
		[CMD_COMM_SET_TELEMETRY_INTERVAL]      ={3, 32},
		[CMD_COMM_GET_TELEMETRY_INTERVAL]      ={1, 32},
		[CMD_COMM_UPDATE_START]                ={4, 32},
		[CMD_COMM_UPDATE_LOAD]                 ={7, 32},
		[CMD_COMM_UPDATE_END]                  ={0, 32},

		////////////////////////////////////////////
		/// CDH
		////////////////////////////////////////////
		//CMD                                 //BODY SIZE //PRIORITY
		[CMD_CDH_PROCESS_HEARTBEAT]            ={0, 2 },
		[CMD_CDH_PROCESS_RUNTIME_ERROR]        ={7, 10},
		[CMD_CDH_PROCESS_COMMAND_ERROR]        ={7, 10},
		[CMD_CDH_PROCESS_NOTIFICATION]         ={1, 2 },
		[CMD_CDH_PROCESS_TELEMETRY_REPORT]     ={7, 3 },
		[CMD_CDH_PROCESS_RETURN]               ={7, 32},
		[CMD_CDH_PROCESS_LED_TEST]             ={2, 4 },

		[CMD_CDH_SET_RTC]                      ={4, 32},
		[CMD_CDH_GET_RTC]                      ={0, 32},

		[CMD_CDH_TEST_FLASH]                   ={0, 32},
		[CMD_CDH_TEST_MRAM]                    ={0, 32},
		[CMD_CDH_TEST_DHARA]                   ={0, 32},
		[CMD_CDH_TEST_STORAGEMANAGER]          ={0, 32},

		[CMD_CDH_RESET_SUBSYSTEM]              ={1, 32},

		[CMD_CDH_ENABLE_ANTENNA]               ={0, 32},
		[CMD_CDH_DEPLOY_ANTENNA]               ={0, 32},

		////////////////////////////////////////////
		/// POWER
		////////////////////////////////////////////
		//CMD                                 //BODY SIZE //PRIORITY
		[CMD_PWR_PROCESS_HEARTBEAT]            ={0, 2 },
		[CMD_PWR_SET_SUBSYSTEM_POWER]          ={2, 0 },
		[CMD_PWR_GET_SUBSYSTEM_POWER]          ={1, 32},
		[CMD_PWR_SET_BATTERY_HEATER_POWER]     ={1, 5 },
		[CMD_PWR_GET_BATTERY_HEATER_POWER]     ={0, 32},
		[CMD_PWR_SET_BATTERY_ACCESS]           ={1, 32},
		[CMD_PWR_GET_BATTERY_ACCESS]           ={0, 32},

		////////////////////////////////////////////
		/// ADCS
		////////////////////////////////////////////
		//CMD                                 //BODY SIZE //PRIORITY
		[CMD_ADCS_SET_MAGNETORQUER_DIRECTION]  ={2, 32},
		[CMD_ADCS_GET_MAGNETORQUER_DIRECTION]  ={1, 32},
		[CMD_ADCS_SET_OPERATING_MODE]          ={1, 32},
		[CMD_ADCS_GET_OPERATING_MODE]          ={0, 32},

		////////////////////////////////////////////
		/// PAYLOAD
		////////////////////////////////////////////
		//CMD                                 //BODY SIZE //PRIORITY
		[CMD_PLD_SET_ACTIVE_ENVS]              ={2, 32},
		[CMD_PLD_GET_ACTIVE_ENVS]              ={0, 32},
		[CMD_PLD_SET_SETPOINT]                 ={5, 32},
		[CMD_PLD_GET_SETPOINT]                 ={1, 32},
		[CMD_PLD_SET_TOLERANCE]                ={4, 32},
		[CMD_PLD_GET_TOLERANCE]                ={0, 32},
		[CMD_PLD_TEST_LEDS]                    ={0, 4 },
};
