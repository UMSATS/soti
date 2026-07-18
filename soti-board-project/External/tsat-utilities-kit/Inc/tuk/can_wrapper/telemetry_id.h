/** (c) 2024 UMSATS
 * @file telemetry_id.h
 */

#ifndef TSAT_UTILITIES_KIT_INC_TUK_CAN_WRAPPER_TELEMETRY_ID_H_
#define TSAT_UTILITIES_KIT_INC_TUK_CAN_WRAPPER_TELEMETRY_ID_H_

#include <assert.h>

typedef enum {
	TEL_PCB_TEMP,
	TEL_MCU_TEMP,
	TEL_RSSI,
	TEL_CONVERTER_STATUS,
	TEL_BATTERY_TEMP,
	TEL_BATTERY_VOLTAGE,
	TEL_BATTERY_CURRENT,
	TEL_COULOMB_COUNT,
	TEL_SOLAR_PANEL_TEMP,
	TEL_SOLAR_PANEL_CURRENT,
	TEL_MAGNETIC_FIELD,
	TEL_ANGULAR_VELOCITY,
	TEL_WELL_TEMP,
	TEL_WELL_LUMINOSITY
} TelemetryID;

_Static_assert(sizeof(TelemetryID) == 1, "Enum size exceeds 1 byte");

// Usage: uint8_t key = CREATE_TELEMETRY_KEY(TEL_PCB_TEMP, 0)
#define CREATE_TELEMETRY_KEY(tel_id, variant_id) (uint8_t)((tel_id << 4) | (0xf & variant_id))

// Usage: TelemetryID tel_id = GET_TELEMETRY_ID(key)
// Usage: uint8_t var_id = GET_VARIANT_ID(key)
#define GET_TELEMETRY_ID(tel_key) (TelemetryID)((tel_key & 0xf0) >> 4)
#define GET_VARIANT_ID(tel_key) (uint8_t)(tel_key & 0x0f)

#endif /* TSAT_UTILITIES_KIT_INC_TUK_CAN_WRAPPER_TELEMETRY_ID_H_ */
