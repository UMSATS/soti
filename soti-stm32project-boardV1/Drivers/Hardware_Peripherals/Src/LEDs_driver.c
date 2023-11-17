/*
 * FILENAME: LEDs_driver.c
 *
 * DESCRIPTION: STM32L4 driver source file for the 3 LEDs.
 *
 * AUTHORS:
 *  - Daigh Burgess (daigh.burgess@umsats.ca)
 *
 * CREATED ON: Mar. 18, 2023
 */

//###############################################################################################
//Include Directives
//###############################################################################################
#include "stm32l4xx_hal.h"
#include "LEDs_driver.h"

//###############################################################################################
//Public Driver Functions
//###############################################################################################
void LEDs_Init()
{
    HAL_GPIO_WritePin(LED4_GPIO, LED4_PIN, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(LED5_GPIO, LED5_PIN, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(LED6_GPIO, LED6_PIN, GPIO_PIN_RESET);
}

void LED4_On()
{
    HAL_GPIO_WritePin(LED4_GPIO, LED4_PIN, GPIO_PIN_SET);
}

void LED5_On()
{
    HAL_GPIO_WritePin(LED5_GPIO, LED5_PIN, GPIO_PIN_SET);
}

void LED6_On()
{
    HAL_GPIO_WritePin(LED6_GPIO, LED6_PIN, GPIO_PIN_SET);
}

void LED4_Off()
{
    HAL_GPIO_WritePin(LED4_GPIO, LED4_PIN, GPIO_PIN_RESET);
}

void LED5_Off()
{
    HAL_GPIO_WritePin(LED5_GPIO, LED5_PIN, GPIO_PIN_RESET);
}

void LED6_Off()
{
    HAL_GPIO_WritePin(LED6_GPIO, LED6_PIN, GPIO_PIN_RESET);
}

void LED4_Toggle()
{
    HAL_GPIO_TogglePin(LED4_GPIO, LED4_PIN);
}

void LED5_Toggle()
{
    HAL_GPIO_TogglePin(LED5_GPIO, LED5_PIN);
}

void LED6_Toggle()
{
    HAL_GPIO_TogglePin(LED6_GPIO, LED6_PIN);
}
