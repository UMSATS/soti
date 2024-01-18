/*
 * LCD_C0216CiZ_driver.h
 *
 *  Created on: Nov 6, 2023
 *      Author: Andrii Kvasnytsia
 */

// Datasheet URL:
// https://newhavendisplay.com/content/specs/NHD-C0216CiZ-FSW-FBW-3V3.pdf

#ifndef HARDWARE_PERIPHERALS_INC_LCD_C0216CIZ_DRIVER_H_
#define HARDWARE_PERIPHERALS_INC_LCD_C0216CIZ_DRIVER_H_

#endif /* HARDWARE_PERIPHERALS_INC_LCD_C0216CIZ_DRIVER_H_ */

// Device I2C Address
#define LCD_ADDR			0x7C

// Register Select
#define LCD_CONTROL_CMD		0x00
#define LCD_CONTROL_DATA	0x40

// Commands
#define LCD_CLEAR 			0x01
#define LCD_RETURN_HOME		0x02
#define LCD_CURSOR_ON		0x0F
#define LCD_CURSOR_OFF		0x0C

void LCD_SEND(uint8_t RS, uint8_t i2c_addr, uint8_t data);

uint8_t LCD_SET_CURSOR(uint8_t position);

void LCD_PRINT_CHAR(unsigned char chr);

void LCD_PRINT_STR(char * str, uint8_t position);

void LCD_INIT(void);
