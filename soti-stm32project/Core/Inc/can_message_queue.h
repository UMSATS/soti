/*
 * FILENAME: can_message_queue.h
 *
 * DESCRIPTION: CAN message queue implementation header file.
 *
 * AUTHORS:
 *  - Om Sevak (om.sevak@umsats.ca)
 *
 * CREATED ON: April 30, 2023
 */

#ifndef INCLUDE_CAN_MESSAGE_QUEUE_H_
#define INCLUDE_CAN_MESSAGE_QUEUE_H_

//###############################################################################################
// Include Directives
//###############################################################################################
#include <stdbool.h>
#include "can.h"

//###############################################################################################
// Define Directives
//###############################################################################################
#define CAN_QUEUE_SIZE 100

//###############################################################################################
// Structs
//###############################################################################################
typedef struct {
    CANMessage_t data;
} CANQueueItem_t;

typedef struct {
    uint32_t head;
    uint32_t tail;
    CANQueueItem_t items[CAN_QUEUE_SIZE];
} CANQueue_t;

//###############################################################################################
// Extern Variables
//###############################################################################################
extern CANQueue_t satelliteToGroundQueue;
extern CANQueue_t groundToSatelliteQueue;

//###############################################################################################
// Public Function Prototypes
//###############################################################################################
/*
 * FUNCTION: CAN_Queue_Init
 *
 * DESCRIPTION: Initialize the given CAN message queue.
 *
 * PARAMETERS:
 *  queue: The CAN message queue.
 */
void CAN_Queue_Init(CANQueue_t* queue);

/*
 * FUNCTION: CAN_Queue_IsEmpty
 *
 * DESCRIPTION: Check if the given CAN message queue is empty.
 *
 * PARAMETERS:
 *  queue: The CAN message queue.
 */
bool CAN_Queue_IsEmpty(const CANQueue_t* queue);

/*
 * FUNCTION: CAN_Queue_IsFull
 *
 * DESCRIPTION: Check if the given CAN message queue is full.
 *
 * PARAMETERS:
 *  queue: The CAN message queue.
 */
bool CAN_Queue_IsFull(const CANQueue_t* queue);

/*
 * FUNCTION: CAN_Queue_Enqueue
 *
 * DESCRIPTION: Enqueue a message into the given CAN message queue.
 *
 * PARAMETERS:
 *  queue: The CAN message queue.
 *  message: The CAN message.
 */
bool CAN_Queue_Enqueue(CANQueue_t* queue, CANMessage_t* message);

/*
 * FUNCTION: CAN_Queue_Dequeue
 *
 * DESCRIPTION: Dequeue a message out of the given CAN message queue.
 *
 * PARAMETERS:
 *  queue: The CAN message queue.
 *  message: The CAN message.
 */
bool CAN_Queue_Dequeue(CANQueue_t* queue, CANMessage_t* message);

#endif /* INCLUDE_CAN_MESSAGE_QUEUE_H_ */
