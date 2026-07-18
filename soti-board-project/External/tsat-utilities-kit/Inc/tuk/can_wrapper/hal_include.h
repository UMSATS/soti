#if defined(STM32L4)
#include "stm32l4xx.h"
#include "stm32l4xx_hal_def.h"
#include "stm32l4xx_hal_can.h"
#include "stm32l4xx_hal_tim.h"

#elif defined(STM32F7)
#include "stm32f7xx.h"
#include "stm32f7xx_hal_def.h"
#include "stm32f7xx_hal_can.h"
#include "stm32f7xx_hal_tim.h"

#else
#error Unsupported STM32 family
#endif
