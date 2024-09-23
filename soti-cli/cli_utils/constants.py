# files
MSG_HISTORY_FILENAME = "messages.json"
CAMERA_DATA_FILENAME = "camera_data.txt"
CAMERA_IMAGE_FILENAME = "images/sat_image.jpeg"

# message size
MSG_SIZE = 11

# soti CAN message sender id
SOTI_SENDER_ID = 0x1

# constants for command codes & priorities
COMM_INFO = {
    # common commands
    0x01: {"priority": None, "dest": None, "name": "ack"},         # ack - priority depends on argument
    0x02: {"priority": None, "dest": None, "name": "nack"},        # nack - priority depends on argument

    # CDH commands
    0x33: {"priority": 0b0011111, "dest": 0x1, "name": "process algae well light level"},
    0x34: {"priority": 0b0000011, "dest": 0x1, "name": "process algae well temperature"},
    0x40: {"priority": 0b0000000, "dest": 0x1, "name": "STM32 reset (CDH)"},
    0x41: {"priority": 0b0111111, "dest": 0x1, "name": "flash storage unit test"},
    0x42: {"priority": 0b0111111, "dest": 0x1, "name": "mram unit test"},
    0x43: {"priority": 0b0000000, "dest": 0x1, "name": "antenna/SPAM deploy 1"},
    0x44: {"priority": 0b0000000, "dest": 0x1, "name": "antenna/SPAM deploy 2"},
    0x45: {"priority": 0b0000111, "dest": 0x1, "name": "take picture"},
    0x47: {"priority": 0b0111111, "dest": 0x1, "name": "get number of tasks"},
    0x48: {"priority": 0b0000111, "dest": 0x1, "name": "sample time-tagged task"},
    0x49: {"priority": 0b0000111, "dest": 0x1, "name": "set RTC"},
    0x4A: {"priority": 0b0111111, "dest": 0x1, "name": "get RTC"},

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
    0x33: "algae-well-light-level",
    0x34: "algae-well-temperature",
}
