# hexadecimal int type
def hexint(x):
    return int(x, 16)

# name for the message history JSON file
MSG_HISTORY_FILENAME = "messages.json"

# constants for command codes

COMM_PRIORITIES = {
    # common commands
    0x01: 0b0001111,    # ack
    0x02: 0b0000111,    # nack
    0x10: 0b0000000,    # shutdown

    # CDH commands
    0x20: 0b0000001,    # heartbeat
    0x30: 0b0000001,    # process battery charge
    0x31: 0b0000001,    # process battery temperature
    0x32: 0b0000001,    # process satellite current consumption
    0x33: 0b0011111,    # process algae well light level
    0x34: 0b0000011,    # process algae well temperature
    0x35: 0b0011111,    # process rotation vector 1
    0x36: 0b0011111,    # process rotation vector 2
    0x40: 0b0000000,    # STM32 reset (CDH)
    0x41: 0b0111111,    # flash storage unit test
    0x42: 0b0111111,    # mram unit test
    0x43: 0b0000000,    # antenna/SPAM deploy
    0x44: 0b0000111,    # take picture
    0x45: 0b0000111,    # send UFH beacon
    0x46: 0b0000111,    # get CDH task list
    0x47: 0b0000111,    # sample time-tagged task

    # PLD commands
    0xA0: 0b0000000,    # STM32 reset (PLD)
    0xA1: 0b0001111,    # LED on
    0xA2: 0b0000111,    # LED off
    0xA3: 0b0000011,    # thermoregulation on
    0xA4: 0b0000001,    # thermoregulation off
    0xA5: 0b0000011,    # heater on
    0xA6: 0b0000001,    # heater off

    # ACDS commands
    0xB0: 0b0001111,    # STM32 reset (ACDS)
    0xB1: 0b0001111,    # magnetorquer 1 full strength
    0xB2: 0b0001111,    # magnetorquer 2 full strength
    0xB3: 0b0000111,    # magnetorquer 3 full strength
    0xB4: 0b0000111,    # magnetorquer 1 off
    0xB5: 0b0000111,    # magnetorquer 2 off
    0xB6: 0b0000111,    # magnetorquer 3 off
    0xB7: 0b0001111,    # magnetorquer 1 forward
    0xB8: 0b0001111,    # magnetorquer 2 forward
    0xB9: 0b0001111,    # magnetorquer 3 forward
    0xBA: 0b0001111,    # magnetorquer 1 reverse
    0xBB: 0b0001111,    # magnetorquer 2 reverse
    0xBC: 0b0001111,    # magnetorquer 3 reverse

    # PWR commands
    0xC0: 0b0000000,    # STM32 reet (PWR)
    0xC1: 0b0000001,    # PLD on
    0xC2: 0b0000000,    # PLD off
    0xC3: 0b0000001,    # ACDS on
    0xC4: 0b0000000,    # ACDS off
    0xC5: 0b0000011,    # battery access on
    0xC6: 0b0000001,    # battery access off
    0xC7: 0b0000011,    # battery heater on
    0xC8: 0b0000001,    # battery heater off
    0xC9: 0b0000111,    # check 3.3V DC-DC converter status
}

# associates the "query" attributes with their command code
# so they can be pulled out of the message history file
QUERY_ATTRS = {
    0x30: "battery-charge",
    0x31: "battery-temperature",
    0x32: "satellite-current-consumption",
    0x33: "algae-well-light-level",
    0x34: "algae-well-temperature",
    0x35: "rotation-vector-1",
    0x36: "rotation-vector-2",
}