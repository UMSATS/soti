#include "can.h"

typedef struct {
    CANMessage_t data;
} CANQueueItem_t;

typedef struct {
    uint32_t head;
    uint32_t tail;
    CANQueueItem_t items[CAN_QUEUE_SIZE];
} CANQueue_t;



bool CAN_Queue_IsEmpty();
bool CAN_Queue_IsFull();
bool CAN_Queue_Enqueue(CANMessage_t* message);
bool CAN_Queue_Dequeue(CANMessage_t* message);

