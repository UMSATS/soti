#ifndef QUEUE_H
#define QUEUE_H

#include <stdbool.h>
#include "can.h"
#include <stdbool.h>

#define CAN_QUEUE_SIZE 100

typedef struct {
    CANMessage_t data;
} CANQueueItem_t;

typedef struct {
    uint32_t head;
    uint32_t tail;
    CANQueueItem_t items[CAN_QUEUE_SIZE];
} CANQueue_t;

void CAN_Queue_Init(CANQueue_t* queue);
bool CAN_Queue_IsEmpty(const CANQueue_t* queue);
bool CAN_Queue_IsFull(const CANQueue_t* queue);
bool CAN_Queue_Enqueue(CANQueue_t* queue, CANMessage_t* message);
bool CAN_Queue_Dequeue(CANQueue_t* queue, CANMessage_t* message);

#endif  QUEUE_H


