/** (c) 2025 UMSATS
 * @file app.c
 */

#include "tuk/tuk.h"

// Constants
#define SERIALIZED_MSG_SIZE 13U
#define QUEUE_SIZE 32U
#define LED_ON_DURATION_MS 20U

// LED thread
extern osThreadId_t LEDThreadHandle;

// UART handle
extern UART_HandleTypeDef huart2;

// Incoming data from the frontend
static uint8_t s_uart_buffer[SERIALIZED_MSG_SIZE];

// Messages to be displayed on the frontend
static osMessageQueueId_t s_output_queue;

// CAN messages queued for transmission
static osMessageQueueId_t s_tx_queue;

// Static function declarations
static void Handle_Message(const CAN_HandleTypeDef*, const CANMessage*);
static void Handle_Error(const CANWrapper_ErrorInfo*);
static void Handle_RX(const CAN_HandleTypeDef*, const CANMessage*, uint8_t*);
static void Handle_TX(const CAN_HandleTypeDef*, const CANMessage*);
static void Serialize_CAN_Message(uint8_t* out_buffer, const CANMessage* in_msg);
static void Deserialize_CAN_Message(CANMessage* out_msg, const uint8_t* in_buffer);

// CAN Wrapper Module configurations.
static const CANWrapper_InitTypeDef CWM_INIT = {
		.hcan = &hcan1,
		.htim = &htim16,

		.message_callback = &Handle_Message,
		.error_callback = &Handle_Error,
		.rx_callback = &Handle_RX,
		.tx_callback = &Handle_TX
};

void App_Init()
{
	s_output_queue = osMessageQueueNew(QUEUE_SIZE, sizeof(CANMessage), NULL);
	s_tx_queue = osMessageQueueNew(QUEUE_SIZE, sizeof(CANMessage), NULL);

	// Prime the UART ISR.
	HAL_UART_Receive_IT(&huart2, s_uart_buffer, sizeof(s_uart_buffer));

	LCD_INIT();
	char *str = "WELCOME TO SOTI!";
	LCD_PRINT_STR(str, 0);
	CANQueue groundToSatelliteQueue = CANQueue_Create();
	HAL_UART_Receive_IT(&huart3, canRxData, sizeof(canRxData));
	CANWrapper_Init(wc_init);
	LEDs_Init();
}

////////////////////////////////////////
/// Event Handlers
////////////////////////////////////////
void Handle_Message(const CAN_HandleTypeDef *hcan, const CANMessage *msg)
{

}

static void Handle_Error(const CANWrapper_ErrorInfo *error)
{

}

static void Handle_RX(const CAN_HandleTypeDef *hcan, const CANMessage *msg, uint8_t *rx_behaviour)
{

}

static void Handle_TX(const CAN_HandleTypeDef *hcan, const CANMessage *msg)
{

}

////////////////////////////////////////
/// Threads
////////////////////////////////////////
/**
 * Uploads messages in the output queue to the frontend via UART.
 */
void App_Main_Thread(void *argument)
{
	CANMessage msg;

	// Infinite loop
	while (1)
	{
		// Wait for the next item in the queue.
		if (osMessageQueueGet(s_output_queue, &msg, NULL, osWaitForever) == osOK)
		{
			// Serialize the message
			uint8_t serialized_data[SERIALIZED_MSG_SIZE];
			Serialize_CAN_Message(serialized_data, &msg);

			// Transmit bytes to frontend.
			HAL_UART_Transmit(&huart2, serialized_data, sizeof(serialized_data), HAL_MAX_DELAY);

			// Light up the LED.
			osThreadFlagsSet(LEDThreadHandle, 1);
		}
	}
}

void App_TX_Thread(void *argument)
{
	CANMessage msg;

	// Infinite loop
	while (1)
	{
		// Wait for the next item in the queue.
		if (osMessageQueueGet(s_tx_queue, &msg, NULL, osWaitForever) == osOK)
		{
			CANWrapper_Transmit_Raw(hcan1, msg, false);
		}
	}
}

/**
 * Lights up the LED for a short period.
 */
void App_LED_Thread(void *argument)
{
	// Infinite loop
	while (1)
	{
		// Block until thread resumed.
		osThreadFlagsWait(1, osFlagsWaitAny, osWaitForever);

		// Turn on LED.
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);

		// Wait.
		osDelay(LED_ON_DURATION_MS);

		if (osThreadFlagsGet() == 0U)
		{
			// Turn off the LED.
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
		}
	}
}

////////////////////////////////////////
/// Helper Functions
////////////////////////////////////////
/**
 * Serializes a CAN message into bytes.
 *
 * @param out_buffer Buffer for storing the result.
 * @param in_msg The message to serialize.
 */
void Serialize_CAN_Message(uint8_t* out_buffer, const CANMessage* in_msg)
{
	memcpy(out_buffer, in_msg, sizeof(CANMessage));
}

/**
 * Deserializes bytes into a CAN message.
 *
 * @param out_msg Message for storing result.
 * @param in_buffer Bytes to deserialize.
 */
void Deserialize_CAN_Message(CANMessage* out_msg, const uint8_t* in_buffer)
{
	memcpy(out_msg, in_buffer, sizeof(CANMessage));

	// Check for inferred fields.
	if (out_msg->body_size == 255)
	{
		out_msg->body_size = CMD_CONFIGS[out_msg->cmd].body_size;
	}
	if (out_msg->priority == 255)
	{
		out_msg->priority = CMD_CONFIGS[out_msg->cmd].priority;
	}
}

////////////////////////////////////////
/// Interrupt Service Routines
////////////////////////////////////////
/**
 * Called when data arrives via UART.
 *
 * @param huart The source peripheral
 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	// Deserialize the received message.
	CANMessage msg;
	Deserialize_CAN_Message(&msg, s_uart_buffer);

	// Enqueue for transmission to the CAN bus.
	osMessageQueuePut(s_tx_queue, &msg, 0U, 0U);

	// Prime the next interrupt.
	HAL_UART_Receive_IT(&huart2, s_uart_buffer, sizeof(s_uart_buffer));
}
