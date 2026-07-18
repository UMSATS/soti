/** (c) 2024 UMSATS
 * @file utils.h
 *
 * Provides useful miscellaneous utilities for all subsystems.
 */

#ifndef TSAT_UTILITIES_KIT_INC_TUK_UTILS_H_
#define TSAT_UTILITIES_KIT_INC_TUK_UTILS_H_

#include <stdint.h>

/**
 * @brief Converts a big-endian (MSB first) buffer of two 8-bit values into a
 *        16-bit value with the processor's native endianness.
 */
static inline uint16_t BE_To_Native_16(const uint8_t *buf)
{
	return (uint16_t)((uint16_t)buf[0] << 8 | (uint16_t)buf[1]);
}

/**
 * @brief Converts a big-endian (MSB first) buffer of four 8-bit values into a
 *        32-bit value with the processor's native endianness.
 */
static inline uint32_t BE_To_Native_32(const uint8_t *buf)
{
	return (uint32_t)buf[0] << 24 |
	       (uint32_t)buf[1] << 16 |
	       (uint32_t)buf[2] << 8 |
	       (uint32_t)buf[3];
}

/**
 * @brief Documents that you are not going to try to recover if an error occurs.
 *
 * If you use IGNORE_FAIL, you are admitting that if the function fails, there
 * is no reasonable way for you to correct the issue, or you don't care one way
 * or the other. This macro has no effect on the behaviour of the code.
 *
 * @note ONLY USE THIS IF YOU HAVE VERIFIED THERE IS NO REASONABLE WAY TO RECOVER.
 *
 * Usage:
 * @code{.c}
 * IGNORE_FAIL(Some_Unreliable_Function());
 * @endcode
 */
#define IGNORE_FAIL(x) (void)(x)

/**
 * @brief Documents that a section of code should never, under any circumstance,
 *        be reached during runtime.
 *
 * Has no effect in release mode, but may print a warning in debug mode if
 * invoked.
 *
 * Usage:
 * @code{.c}
 * UNREACHABLE();
 * @endcode
 */
#define UNREACHABLE() (void)(0)

#endif /* TSAT_UTILITIES_KIT_INC_TUK_UTILS_H_ */
