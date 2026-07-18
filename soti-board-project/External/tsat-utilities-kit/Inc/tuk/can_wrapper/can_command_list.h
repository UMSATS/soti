/** (c) 2024 UMSATS
 * @file can_command_list.h
 *
 * Configurations for all valid command ID's.
 */

#ifndef CAN_WRAPPER_MODULE_INC_CAN_COMMAND_LIST_H_
#define CAN_WRAPPER_MODULE_INC_CAN_COMMAND_LIST_H_

#include "telemetry_id.h"

#include <stdint.h>
#include <assert.h>

// Used in the PROCESS_NOTIFICATION command.
typedef enum
{
	NOTIFICATION_STARTUP,
	NOTIFICATION_PREPARING_FOR_SHUTDOWN,
	NOTIFICATION_READY_FOR_SHUTDOWN
} NotificationID;
_Static_assert(sizeof(NotificationID) == 1, "Enum size is not 8 bits");

// NOTE: If you modify this list, you MUST update the command configurations to
// reflect your changes.
typedef enum
{
	////////////////////////////////////////////
	/// COMMON
	////////////////////////////////////////////
	CMD_COMM_RESET,
	CMD_COMM_PREPARE_FOR_SHUTDOWN,
	CMD_COMM_GET_TELEMETRY,
	CMD_COMM_SET_TELEMETRY_INTERVAL,
	CMD_COMM_GET_TELEMETRY_INTERVAL,
	CMD_COMM_UPDATE_START,
	CMD_COMM_UPDATE_LOAD,
	CMD_COMM_UPDATE_END,

	////////////////////////////////////////////
	/// CDH
	////////////////////////////////////////////
	// Event Processing.
	CMD_CDH_PROCESS_HEARTBEAT,
	CMD_CDH_PROCESS_RUNTIME_ERROR,
	CMD_CDH_PROCESS_COMMAND_ERROR,
	CMD_CDH_PROCESS_NOTIFICATION,
	CMD_CDH_PROCESS_TELEMETRY_REPORT,
	CMD_CDH_PROCESS_RETURN,
	CMD_CDH_PROCESS_LED_TEST,

	// Clock
	CMD_CDH_SET_RTC,
	CMD_CDH_GET_RTC,

	// Tests
	CMD_CDH_TEST_FLASH,
	CMD_CDH_TEST_MRAM,
	CMD_CDH_TEST_DHARA,
	CMD_CDH_TEST_STORAGEMANAGER,

	CMD_CDH_RESET_SUBSYSTEM,

	// Antenna
	CMD_CDH_ENABLE_ANTENNA,
	CMD_CDH_DEPLOY_ANTENNA,

	////////////////////////////////////////////
	/// POWER
	////////////////////////////////////////////
	CMD_PWR_PROCESS_HEARTBEAT,
	CMD_PWR_SET_SUBSYSTEM_POWER,
	CMD_PWR_GET_SUBSYSTEM_POWER,
	CMD_PWR_SET_BATTERY_HEATER_POWER,
	CMD_PWR_GET_BATTERY_HEATER_POWER,
	CMD_PWR_SET_BATTERY_ACCESS,
	CMD_PWR_GET_BATTERY_ACCESS,

	////////////////////////////////////////////
	/// ADCS
	////////////////////////////////////////////
	CMD_ADCS_SET_MAGNETORQUER_DIRECTION,
	CMD_ADCS_GET_MAGNETORQUER_DIRECTION,
	CMD_ADCS_SET_OPERATING_MODE,
	CMD_ADCS_GET_OPERATING_MODE,

	////////////////////////////////////////////
	/// PAYLOAD
	////////////////////////////////////////////
	CMD_PLD_SET_ACTIVE_ENVS,
	CMD_PLD_GET_ACTIVE_ENVS,
	CMD_PLD_SET_SETPOINT,
	CMD_PLD_GET_SETPOINT,
	CMD_PLD_SET_TOLERANCE,
	CMD_PLD_GET_TOLERANCE,
	CMD_PLD_TEST_LEDS,

	NUM_COMMANDS
} CmdID;
_Static_assert(sizeof(CmdID) == 1, "Enum size exceeds 1 byte");

typedef struct
{
	uint8_t body_size;
	uint8_t priority;
} CmdConfig;

extern const CmdConfig CMD_CONFIGS[NUM_COMMANDS];

#endif /* CAN_WRAPPER_MODULE_INC_CAN_COMMAND_LIST_H_ */
