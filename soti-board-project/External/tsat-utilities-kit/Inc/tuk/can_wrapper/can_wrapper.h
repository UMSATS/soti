/** (c) 2024 UMSATS
 * @file can_wrapper.h
 *
 * CAN wrapper for simplified CAN transmission & reception.
 */

#ifndef CAN_WRAPPER_MODULE_INC_CAN_WRAPPER_H_
#define CAN_WRAPPER_MODULE_INC_CAN_WRAPPER_H_

#include "cwm_api.h"
#include "hal_include.h"
#include "can_command_list.h"
#include "can_message.h"
#include "error_info.h"
#include "telemetry_id.h"

#include "tuk/error_list.h"

#include "cmsis_os.h"

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

// Constants for RX callback.
#define RX_ACK            0b001
#define RX_HANDLE         0b010
#define RX_CLEAR_TX_STORE 0b100

typedef void (*CANMessageCallback)(const CAN_HandleTypeDef*, const CANMessage*);

#ifdef CWM_API_ADVANCED
typedef void (*CANRXCallback)(const CAN_HandleTypeDef*, const CANMessage*, uint8_t*);
typedef void (*CANTXCallback)(const CAN_HandleTypeDef*, const CANMessage*);
#endif

typedef void (*CANErrorCallback)(const CANWrapper_ErrorInfo*);

typedef struct
{
#ifdef CWM_API_STANDARD
	NodeID node_id; // Your subsystem's unique ID in the network.
#endif

	CANMessageCallback message_callback; // Called when a message is ready to be handled.
	CANErrorCallback error_callback; // Called on internal error.

#ifdef CWM_API_ADVANCED
	CANRXCallback rx_callback; // Called when a message is immediately received.
	CANTXCallback tx_callback; // Called on message transmission.
#endif
} CANWrapper_InitTypeDef;

/**
 * Performs necessary setup for normal functioning.
 *
 * Initialises the module by configuring the designated peripherals and creating
 * private RTOS objects. Call this function in an appropriate place between
 * `osKernelInitialize()` and `osKernelStart()`.
 *
 * @warning This function should not be called from an ISR.
 *
 * @param init_struct Configuration for initialisation.
 * @return Error code or ERR_OK on success.
 */
ErrorCode CANWrapper_Init(const CANWrapper_InitTypeDef *init_struct);

/**
 * Configures and starts a CAN peripheral for operation with the module.
 *
 * @warning This function should not be called from an ISR.
 *
 * @param hcan The CAN peripheral.
 * @return Error code or ERR_OK on success.
 */
ErrorCode CANWrapper_CAN_Start(CAN_HandleTypeDef *hcan);

#ifdef CWM_API_STANDARD
/**
 * Sends a message using the TSAT protocol.
 *
 * Loads a message into one of the three TX mailboxes. In most cases, this
 * function is non-blocking. However, if the mailboxes are full, this function
 * will block for a short time until either space is made or a timeout occurs,
 * in which case an appropriate error is returned.
 *
 * See the TSAT command reference for details about commands & structure.
 *
 * @warning This function can fail if called from an ISR. Avoid doing so unless
 *     you have error handling in place with a recovery strategy.
 *
 * @param target The ID of the receiving node.
 * @param cmd    The command being sent. This dictates the contents of `body`.
 * @param body   The bytes comprising the message body.
 * @return Error code or ERR_OK on success.
 */
ErrorCode CANWrapper_Transmit(CAN_HandleTypeDef *hcan, NodeID target, CmdID cmd, const uint8_t *body);

#elif defined(CWM_API_ADVANCED)
/**
 * Sends a raw CAN message formatted in accordance with the TSAT protocol.
 *
 * Similar to `CANWrapper_Transmit` but permits any message, irrespective of
 * validity or context.
 *
 * @warning This function can fail if called from an ISR. Avoid doing so unless
 *     you have error handling in place with a recovery strategy.
 *
 * @param hcan           The CAN peripheral.
 * @param msg            The message to send.
 * @param strict_timeout Whether to expect an ACK within the timeout.
 * @return Error code or ERR_OK on success.
 */
ErrorCode CANWrapper_Transmit_Raw(CAN_HandleTypeDef *hcan, const CANMessage *msg, bool strict_timeout);
#endif

#endif /* CAN_WRAPPER_MODULE_INC_CAN_WRAPPER_H_ */
