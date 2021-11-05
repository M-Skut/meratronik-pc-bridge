#pragma once
#include <stdint.h>
#include <Arduino.h>

/*
 * Pin definitions added for more code readability.
 */

namespace Pins {
	// TODO: constexpr those
	// Least significant digit, least significant bit
	#define PIN_DIGIT0_0 (PC0)
	#define PIN_DIGIT0_1 (PC1)
	#define PIN_DIGIT0_2 (PC2)
	// Least significant digit, most significant bit
	#define PIN_DIGIT0_3 (PC3)
	// Similarly for the rest
	#define PIN_DIGIT1_0 (PA0)
	#define PIN_DIGIT1_1 (PA1)
	//CHANGED
	#define PIN_DIGIT1_2 (PA10) //(PA2)
	#define PIN_DIGIT1_3 (PC4) //(PA3)

	#define PIN_DIGIT2_0 (PC9)
	#define PIN_DIGIT2_1 (PC10)
	#define PIN_DIGIT2_2 (PC11)
	#define PIN_DIGIT2_3 (PC12)

	#define PIN_DIGIT3_0 (PB12)
	#define PIN_DIGIT3_1 (PB13)
	#define PIN_DIGIT3_2 (PB14)
	#define PIN_DIGIT3_3 (PB15)

	// Most significant digit (1 bit only)
	#define PIN_DIGIT4_0 (PA4)

	// Status pins
	#define PIN_MEASURE_PLUS (PA8)
	#define PIN_MEASURE_MINUS (PA9)
	#define PIN_DC_MEASURE (PB8)
	#define PIN_AC_MEASURE (PB9)
	#define PIN_OVERRANGE (PB6)

	// Measurement range pins
	#define PIN_RANGE_A (PB3)
	#define PIN_RANGE_B (PB4)
	#define PIN_RANGE_C (PB5)

	// Control pins
	#define PIN_STOP_MEASURE  (PA15) //(PA13)
	#define PIN_START_MEASURE (PB7) //(PA14)
	#define PIN_BLOCK_MEASURE (PC13)// (PA15)

	enum measurement_type {
		DC_MEASURE,
		AC_MEASURE,
		TYPE_UNDEFINED
	};

	enum measurement_sign {
		MEASURE_PLUS ,
		MEASURE_MINUS,
		SIGN_UNDEFINED
	};

	enum measurement_range {
		HUNDRED_MV,
		ONE_V,
		TEN_V ,
		HUNDRED_V,
		THOUSAND_V,
		OVERRANGE,
		RANGE_UNDEFINED
	};

	enum error_type {
		DIGIT0_NOT_BCD = -1,
		DIGIT1_NOT_BCD = -2,
		DIGIT2_NOT_BCD = -3,
		DIGIT3_NOT_BCD = -4,
		INVALID_MEASUREMENT_RANGE = -10,
		INVALID_MEASUREMENT_TYPE = -20,
		INVALID_MEASUREMENT_SIGN = -30,

	};

	// Source of order of those values can be found in technical
	// description of Meratronik V-541
	// XXX: Modified to work with our specimen
	measurement_type type_from_bits[] = {
			DC_MEASURE, DC_MEASURE, AC_MEASURE, TYPE_UNDEFINED
	};

	measurement_sign sign_from_bits[] = {
			MEASURE_PLUS, MEASURE_PLUS, MEASURE_MINUS, SIGN_UNDEFINED
	};

	// This specific range table is taken from Meratronik V-543 manual
	// XXX: Modified to work with for our specimen
	measurement_range range_from_bits[] = {
			OVERRANGE, OVERRANGE, OVERRANGE, OVERRANGE,
			OVERRANGE, OVERRANGE, OVERRANGE, OVERRANGE,
			HUNDRED_V, ONE_V, THOUSAND_V, TEN_V,
			HUNDRED_MV, RANGE_UNDEFINED, RANGE_UNDEFINED, RANGE_UNDEFINED
	};

	const char range_to_char[] = {
			'A', 'B', 'C', 'D', 'E', 'O',
			'Z' // This should never be sent
	};

	const char type_to_char[] = {
			'A', 'D',
			'Z' // This should never be sent
	};

	const char sign_to_char[] = {
			'P', 'M',
			'Z' // This should never be sent
	};

	const uint8_t input_pins[] = {
			PIN_DIGIT0_0, PIN_DIGIT0_1, PIN_DIGIT0_2, PIN_DIGIT0_3,
			PIN_DIGIT1_0, PIN_DIGIT1_1, PIN_DIGIT1_2, PIN_DIGIT1_3,
			PIN_DIGIT2_0, PIN_DIGIT2_1, PIN_DIGIT2_2, PIN_DIGIT2_3,
			PIN_DIGIT3_0, PIN_DIGIT3_1, PIN_DIGIT3_2, PIN_DIGIT3_3,
			PIN_DIGIT4_0,
			PIN_MEASURE_PLUS, PIN_MEASURE_MINUS, PIN_DC_MEASURE, PIN_AC_MEASURE, PIN_OVERRANGE,
			PIN_RANGE_A, PIN_RANGE_B, PIN_RANGE_C,
	};

	const uint8_t digit0_pins[] = {
			PIN_DIGIT0_0, PIN_DIGIT0_1, PIN_DIGIT0_2, PIN_DIGIT0_3,
	};
	const uint8_t digit1_pins[] = {
			PIN_DIGIT1_0, PIN_DIGIT1_1, PIN_DIGIT1_2, PIN_DIGIT1_3,
	};
	const uint8_t digit2_pins[] = {
			PIN_DIGIT2_0, PIN_DIGIT2_1, PIN_DIGIT2_2, PIN_DIGIT2_3,
	};
	const uint8_t digit3_pins[] = {
			PIN_DIGIT3_0, PIN_DIGIT3_1, PIN_DIGIT3_2, PIN_DIGIT3_3,
	};

	const uint8_t output_pins[] = {
			PIN_STOP_MEASURE, PIN_START_MEASURE, PIN_BLOCK_MEASURE
	};

	const uint8_t pins_high_default[] = {PIN_STOP_MEASURE, PIN_BLOCK_MEASURE};
	const uint8_t pins_low_default[] = {PIN_START_MEASURE};

}

