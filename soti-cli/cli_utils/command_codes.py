# constants for command codes

# common commands
COMMON = {
    "ack": 0x01,
    "nack": 0x02,
    "shutdown": 0x10
}

# CDH commands
CDH = {
    "heartbeat": 0x20,
    "process_battery_charge": 0x30,
    "process_battery_temperature": 0x31,
    "process_satellite_current_consumption": 0x32,
    "process_algae_well_light_level": 0x33,
    "process_algae_well_temperature": 0x34,
    "process_rotation_vector_1": 0x35,
    "process_rotation_vector_2": 0x36,
    "stm32_reset": 0x40,
    "flash_storage_unit_test": 0x41,
    "mram_unit_test": 0x42,
    "antenna_spam_deploy": 0x43,
    "take_picture": 0x44,
    "send_ufh_beacon": 0x45,
    "get_cdh_task_list": 0x46,
    "sample_time_tagged_task": 0x47
}

PLD = {
    "stm32_reset": 0xA0,
    "led_on": 0xA1,
    "led_off": 0xA2,
    "thermoregulation_on": 0xA3,
    "thermoregulation_off": 0xA4,
    "heater_on": 0xA5,
    "heater_off": 0xA6,
}

ACDS = {
    "stm32_reset": 0xB0,
    "magnetorquer_1_full_strength": 0xB1,
    "magnetorquer_2_full_strength": 0xB2,
    "magnetorquer_3_full_strength": 0xB3,
    "magnetorquer_1_off": 0xB4,
    "magnetorquer_2_off": 0xB5,
    "magnetorquer_3_off": 0xB6,
    "magnetorquer_1_forward": 0xB7,
    "magnetorquer_2_forward": 0xB8,
    "magnetorquer_3_forward": 0xB9,
    "magnetorquer_1_reverse": 0xBA,
    "magnetorquer_2_reverse": 0xBB,
    "magnetorquer_3_reverse": 0xBC,
}

PWR = {
    "stm32_reset": 0xC0,
    "pld_on": 0xC1,
    "pld_off": 0xC2,
    "adcs_on": 0xC3,
    "acds_off": 0xC4,
    "battery_access_on": 0xC5,
    "battery_access_off": 0xC6,
    "battery_heater_on": 0xC7,
    "battery_heater_off": 0xC8,
    "check_converter_status": 0xC9,
}