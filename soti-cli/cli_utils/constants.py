# files
MSG_HISTORY_FILENAME = "messages.json"
CAMERA_DATA_FILENAME = "camera_data.txt"
CAMERA_IMAGE_FILENAME = "sat_image.jpeg"

# message size
MSG_SIZE = 11

# soti CAN message sender id
SOTI_SENDER_ID = 0x1

# constants for command codes & priorities
COMM_INFO = {
    # common commands
    0x01: {"priority": None, "dest": None, "name": "ack"},         # ack - priority depends on argument
    0x02: {"priority": None, "dest": None, "name": "nack"},         # nack - priority depends on argument
    0x10: {"priority": 0b0000000, "dest": 0x07, "name": "shutdown"},    # shutdown

    # CDH commands
    0x20: {"priority": 0b0000001, "dest": 0x1, "name": "heartbeat"},
    0x30: {"priority": 0b0000001, "dest": 0x1, "name": "process battery charge"},
    0x31: {"priority": 0b0000001, "dest": 0x1, "name": "process battery temperature"},
    0x32: {"priority": 0b0000001, "dest": 0x1, "name": "process satellite current consumption"},
    0x33: {"priority": 0b0011111, "dest": 0x1, "name": "process algae well light level"},
    0x34: {"priority": 0b0000011, "dest": 0x1, "name": "process algae well temperature"},
    0x35: {"priority": 0b0011111, "dest": 0x1, "name": "process rotation vector 1"},
    0x36: {"priority": 0b0011111, "dest": 0x1, "name": "process rotation vector 2"},
    0x40: {"priority": 0b0000000, "dest": 0x1, "name": "STM32 reset (CDH)"},
    0x41: {"priority": 0b0111111, "dest": 0x1, "name": "flash storage unit test"},
    0x42: {"priority": 0b0111111, "dest": 0x1, "name": "mram unit test"},
    0x43: {"priority": 0b0000000, "dest": 0x1, "name": "antenna/SPAM deploy 1"},
    0x44: {"priority": 0b0000000, "dest": 0x1, "name": "antenna/SPAM deploy 2"},
    0x45: {"priority": 0b0000111, "dest": 0x1, "name": "take picture"},
    0x46: {"priority": 0b0000111, "dest": 0x1, "name": "send UFH beacon"},
    0x47: {"priority": 0b0000111, "dest": 0x1, "name": "get CDH task list"},
    0x48: {"priority": 0b0000111, "dest": 0x1, "name": "sample time-tagged task"},
    0x49: {"priority": 0b0000111, "dest": 0x1, "name": "set internal rtc"},
    0x4A: {"priority": 0b0111111, "dest": 0x1, "name": "get internal rtc"},
    0x50: {"priority": 0b0000000, "dest": 0x1, "name": "PLD error report"},
    0x51: {"priority": 0b0000000, "dest": 0x1, "name": "ADCS error report"},
    0x52: {"priority": 0b0000000, "dest": 0x1, "name": "PWR error report"},

    # PLD commands
    0xA0: {"priority": 0b0000000, "dest": 0x3, "name": "STM32 reset (PLD)"},
    0xA1: {"priority": 0b0001111, "dest": 0x3, "name": "LED on"},
    0xA2: {"priority": 0b0000111, "dest": 0x3, "name": "LED off"},
    0xA3: {"priority": 0b0000011, "dest": 0x3, "name": "thermoregulation on"},
    0xA4: {"priority": 0b0000001, "dest": 0x3, "name": "thermoregulation off"},
    0xA5: {"priority": 0b0000011, "dest": 0x3, "name": "heater on"},
    0xA6: {"priority": 0b0000001, "dest": 0x3, "name": "heater off"},

    # ACDS commands
    0xB0: {"priority": 0b0001111, "dest": 0x2, "name": "STM32 reset (ACDS)"},
    0xB1: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 1 full strength"},
    0xB2: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 2 full strength"},
    0xB3: {"priority": 0b0000111, "dest": 0x2, "name": "magnetorquer 3 full strength"},
    0xB4: {"priority": 0b0000111, "dest": 0x2, "name": "magnetorquer 1 off"},
    0xB5: {"priority": 0b0000111, "dest": 0x2, "name": "magnetorquer 2 off"},
    0xB6: {"priority": 0b0000111, "dest": 0x2, "name": "magnetorquer 3 off"},
    0xB7: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 1 forward"},
    0xB8: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 2 forward"},
    0xB9: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 3 forward"},
    0xBA: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 1 reverse"},
    0xBB: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 2 reverse"},
    0xBC: {"priority": 0b0001111, "dest": 0x2, "name": "magnetorquer 3 reverse"},

    # PWR commands
    0xC0: {"priority": 0b0000000, "dest": 0x0, "name": "STM32 reet (PWR)"},
    0xC1: {"priority": 0b0000001, "dest": 0x0, "name": "PLD on"},
    0xC2: {"priority": 0b0000000, "dest": 0x0, "name": "PLD off"},
    0xC3: {"priority": 0b0000001, "dest": 0x0, "name": "ACDS on"},
    0xC4: {"priority": 0b0000000, "dest": 0x0, "name": "ACDS off"},
    0xC5: {"priority": 0b0000011, "dest": 0x0, "name": "battery access on"},
    0xC6: {"priority": 0b0000001, "dest": 0x0, "name": "battery access off"},
    0xC7: {"priority": 0b0000011, "dest": 0x0, "name": "battery heater on"},
    0xC8: {"priority": 0b0000001, "dest": 0x0, "name": "battery heater off"},
    0xC9: {"priority": 0b0000111, "dest": 0x0, "name": "check 3.3V DC-DC converter status"},
}

# associates a sender id with a human-readable sender for message history
SYSTEM_IDS = {
    0x0: "PCU",
    0x1: "CDH/Comms",
    0x2: "ACDS",
    0x3: "Payload",
    0xFF: "SOTI",
}

# associates the "query" attributes with their command code
# so they can be pulled out of the message history file
QUERY_ATTRS = {
    0x01: "ack",
    0x30: "battery-charge",
    0x31: "battery-temperature",
    0x32: "satellite-current-consumption",
    0x33: "algae-well-light-level",
    0x34: "algae-well-temperature",
    0x35: "rotation-vector-1",
    0x36: "rotation-vector-2",
}
