/*
 *  LCD_C0216CiZ_driver.c
 *
 *  Created on: Nov 6, 2023
 *  Author: Andrii Kvasnytsia
 */

// Datasheet URL:
// https://newhavendisplay.com/content/specs/NHD-C0216CiZ-FSW-FBW-3V3.pdf

#include "stm32l4xx_hal.h"
#include "LCD_C0216CiZ_driver.h"
#include "main.h"

extern I2C_HandleTypeDef hi2c3;

void LCD_SEND(uint8_t ControlByte, uint8_t i2c_addr, uint8_t data){
	uint8_t Data[2];

	Data[0] = ControlByte;
	Data[1] = data;

	HAL_I2C_Master_Transmit(&hi2c3, (uint16_t)i2c_addr, Data, 2, 50);
}

uint8_t LCD_SET_CURSOR(uint8_t position){
	if(position > 31) return 0;

	if(position <= 15){
		// 1st line
		LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x80 + position);
	}
	else{
		// 2nd line
		LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0xC0 + position - 16);
	}

	return 1;
}

void LCD_PRINT_CHAR(unsigned char chr){
	LCD_SEND(LCD_CONTROL_DATA, LCD_ADDR, (uint8_t)chr);
}

void LCD_PRINT_STR(char * str, uint8_t position){
	while(*str){
		if(LCD_SET_CURSOR(position)){

			LCD_PRINT_CHAR(*str++);

			position++;
		}
	}
}

void LCD_CLEAR_DISPLAY(void){
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, LCD_CLEAR);
}

void LCD_INIT(void){
	HAL_GPIO_WritePin(LCD_nReset_GPIO_Port, LCD_nReset_Pin, GPIO_PIN_SET);

	HAL_Delay(60);

	/* Wake up call */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x38);
	HAL_Delay(10);

	/*
	 * Function Set
	 * 8 bit interface; 2 lines; Instruction table 1
	 */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x39);
	HAL_Delay(10);

	/*
	 * Internal OSC frequency
	 * BS = 0; 1/5 bias
	 */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x14);

	/* Contrast set */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x71);

	/*
	 * ICON Display		ON
	 * Booster circuit	ON
	 */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x5E);

	/*
	 * Follower circuit	ON
	 */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x6C);

	/*
	 * Entire display	ON
	 * Cursor			OFF
	 * Cursor position	OFF
	 */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, LCD_CURSOR_OFF);

	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, LCD_CLEAR);

	/* Entry mode set */
	LCD_SEND(LCD_CONTROL_CMD, LCD_ADDR, 0x06);
}
