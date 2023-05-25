# well-known help messages for commands
help_message = """
Use \"-h\" with any operation for specific help.
send: sends a command to the board
query: retrieves information from the board
exit: exits the program
"""

command_map = """
Available commands:

=== Common ===
ack
nack
shutdown

=== CDH ===
heartbeat
process_battery_charge
process_battery_temperature
process_satellite_current_consumption
process_algae_well_light_level
process_algae_well_temperature
process_rotation_vector_1
process_rotation_vector_2
cdh_stm32_reset
flash_storage_unit_test
mram_unit_test
antenna_spam_deploy
take_picture
send_ufh_beacon
get_cdh_task_list
sample_time_tagged_task

=== PLD ===
pld_stm32_reset
led_on
led_off
thermoregulation_on
thermoregulation_off
heater_on
heater_off

== ACDS ===
acds_stm32_reset
magnetorquer_1_full_strength
magnetorquer_2_full_strength
magnetorquer_3_full_strength
magnetorquer_1_off
magnetorquer_2_off
magnetorquer_3_off
magnetorquer_1_forward
magnetorquer_2_forward
magnetorquer_3_forward
magnetorquer_1_reverse
magnetorquer_2_reverse
magnetorquer_3_reverse

=== PWR ===
pwr_stm32_reset
pld_on
pld_off
acds_on
acds_off
battery_access_on
battery_access_off
battery_heater_on
battery_heater_off
check_converter_status
"""
