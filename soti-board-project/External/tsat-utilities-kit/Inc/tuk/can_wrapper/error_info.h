/** (c) 2024 UMSATS
 * @file error_info.h
 */

#ifndef TSAT_UTILITIES_KIT_INC_TUK_CAN_WRAPPER_ERROR_INFO_H_
#define TSAT_UTILITIES_KIT_INC_TUK_CAN_WRAPPER_ERROR_INFO_H_

#include "can_message.h"

typedef struct
{
	enum
	{
		CAN_WRAPPER_ERROR_TIMEOUT = 0,
		CAN_WRAPPER_ERROR_CAN_TIMEOUT,
	} error;
	union
	{
		CANMessage msg;
		// TODO: more error information.
	};
} CANWrapper_ErrorInfo;

#endif /* TSAT_UTILITIES_KIT_INC_TUK_CAN_WRAPPER_ERROR_INFO_H_ */
