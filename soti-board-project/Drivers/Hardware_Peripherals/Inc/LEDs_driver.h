/*
 * FILENAME: LEDs_driver.h
 *
 * DESCRIPTION: STM32L4 driver header file for the 3 LEDs.
 *
 * AUTHORS:
 *  - Daigh Burgess (daigh.burgess@umsats.ca)
 *
 * CREATED ON: Mar. 18, 2023
 */

#ifndef HARDWARE_PERIPHERALS_INC_LEDS_DRIVER_H_
#define HARDWARE_PERIPHERALS_INC_LEDS_DRIVER_H_

//###############################################################################################
//Include Directives
//###############################################################################################
#include "stm32l4xx_hal.h"

//###############################################################################################
//Public Define Directives
//###############################################################################################
#define LED4_GPIO     GPIOB
#define LED4_PIN      GPIO_PIN_12

#define LED5_GPIO     GPIOB
#define LED5_PIN      GPIO_PIN_13

#define LED6_GPIO     GPIOB
#define LED6_PIN      GPIO_PIN_14

//###############################################################################################
//Public Driver Function Prototypes
//###############################################################################################
/*
 * FUNCTION: LEDs_Init
 *
 * DESCRIPTION: Turn all 3 LEDs off.
 */
void LEDs_Init();

/*
 * FUNCTION: LED4_On
 *
 * DESCRIPTION: Turn LED4 on.
 */
void LED4_On();

/*
 * FUNCTION: LED5_On
 *
 * DESCRIPTION: Turn LED5 on.
 */
void LED5_On();

/*
 * FUNCTION: LED6_On
 *
 * DESCRIPTION: Turn LED6 on.
 */
void LED6_On();

/*
 * FUNCTION: LED4_Off
 *
 * DESCRIPTION: Turn LED4 off.
 */
void LED4_Off();

/*
 * FUNCTION: LED5_Off
 *
 * DESCRIPTION: Turn LED5 off.
 */
void LED5_Off();

/*
 * FUNCTION: LED6_Off
 *
 * DESCRIPTION: Turn LED6 off.
 */
void LED6_Off();

/*
 * FUNCTION: LED4_Toggle
 *
 * DESCRIPTION: Toggle LED4.
 */
void LED4_Toggle();

/*
 * FUNCTION: LED5_Toggle
 *
 * DESCRIPTION: Toggle LED5.
 */
void LED5_Toggle();

/*
 * FUNCTION: LED6_Toggle
 *
 * DESCRIPTION: Toggle LED6.
 */
void LED6_Toggle();

#endif /* HARDWARE_PERIPHERALS_INC_LEDS_DRIVER_H_ */
