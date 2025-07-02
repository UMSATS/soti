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

void App_Init()
{
	s_output_queue = osMessageQueueNew(QUEUE_SIZE, sizeof(CANMessage), NULL);

	// Prime the UART ISR.
	HAL_UART_Receive_IT(&huart2, s_uart_buffer, sizeof(s_uart_buffer));
}

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
/// Interrupt Service Routines
////////////////////////////////////////
/**
  * @brief  EXTI line detection callback.
  * @param  GPIO_Pin Specifies the port pin connected to corresponding EXTI line.
  * @retval None
  */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	// Check if the push button has been pressed.
	if (GPIO_Pin == GPIO_PIN_13)
	{
		// Create a fake message and send to frontend.
		CANMessage msg = {
				.cmd = CMD_CDH_PROCESS_TELEMETRY_REPORT
		};
		osMessageQueuePut(s_output_queue, &msg, 0U, 0U);
	}
}

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

	// Relay back to frontend.
	osMessageQueuePut(s_output_queue, &msg, 0U, 0U);

	// Prime the next interrupt.
	HAL_UART_Receive_IT(&huart2, s_uart_buffer, sizeof(s_uart_buffer));
}
