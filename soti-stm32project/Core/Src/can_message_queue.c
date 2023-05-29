/*
 * FILENAME: can_message_queue.c
 *
 * DESCRIPTION: CAN message queue implementation source file.
 *
 * AUTHORS:
 *  - Om Sevak (om.sevak@umsats.ca)
 *
 * CREATED ON: April 30, 2023
 */

//###############################################################################################
// Include Directives
//###############################################################################################
#include <string.h>
#include <stdbool.h>
#include "can.h"
#include "can_message_queue.h"

//###############################################################################################
//Public Functions
//###############################################################################################
void CAN_Queue_Init(CANQueue_t* queue) {
    queue->head = 0;
    queue->tail = 0;
}

bool CAN_Queue_IsEmpty(const CANQueue_t* queue) {
    return (queue->head == queue->tail);
}

bool CAN_Queue_IsFull(const CANQueue_t* queue) {
    return ((queue->tail + 1) % CAN_QUEUE_SIZE == queue->head);
}

bool CAN_Queue_Enqueue(CANQueue_t* queue, CANMessage_t* message) {
    if (CAN_Queue_IsFull(queue)) {
        return false;
    }

    CANQueueItem_t* item = &queue->items[queue->tail];
    memcpy(&item->data, message, sizeof(CANMessage_t));
    queue->tail = (queue->tail + 1) % CAN_QUEUE_SIZE;

    return true;
}

bool CAN_Queue_Dequeue(CANQueue_t* queue, CANMessage_t* messageBuffer) {
    if (CAN_Queue_IsEmpty(queue)) {
        return false;
    }

    CANQueueItem_t* item = &queue->items[queue->head];
    memcpy(messageBuffer, &item->data, sizeof(CANMessage_t));
    queue->head = (queue->head + 1) % CAN_QUEUE_SIZE;

    return true;
}
