#include "can_message_queue.h"

#include <string.h>


CANQueue_t can_queue;

void CAN_Queue_Init() {
    can_queue.head = 0;
    can_queue.tail = 0;
}

bool CAN_Queue_IsEmpty() {
    return (can_queue.head == can_queue.tail);
}

bool CAN_Queue_IsFull() {
    return ((can_queue.tail + 1) % CAN_QUEUE_SIZE == can_queue.head);
}

bool CAN_Queue_Enqueue(CANMessage_t* message) {
    if (CAN_Queue_IsFull()) {
        return false;
    }

    CANQueueItem_t* item = &can_queue.items[can_queue.tail];
    memcpy(&item->data, message, sizeof(CANMessage_t));
    can_queue.tail = (can_queue.tail + 1) % CAN_QUEUE_SIZE;

    return true;
}

bool CAN_Queue_Dequeue(CANMessage_t* message) {
    if (CAN_Queue_IsEmpty()) {
        return false;
    }

    CANQueueItem_t* item = &can_queue.items[can_queue.head];
    memcpy(message, &item->data, sizeof(CANMessage_t));
    can_queue.head = (can_queue.head + 1) % CAN_QUEUE_SIZE;

    return true;
}
