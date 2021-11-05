#pragma once

/*
 * various utility functions
 */

#include <Arduino.h>
#include <pins.h>
#include <stdint.h>

namespace IOUtils {
	uint8_t BCDToDecimal(uint8_t bcd_value) {
		return (bcd_value & 0x0F);
	}

	void initPins(void) {
		for (uint8_t pin : Pins::input_pins) pinMode(pin, INPUT);
		for (uint8_t pin : Pins::output_pins) pinMode(pin, OUTPUT);
		for (uint8_t pin : Pins::pins_high_default) digitalWrite(pin, HIGH);
		for (uint8_t pin : Pins::pins_low_default) digitalWrite(pin, LOW);
	}

	// Gets value displayed on the meter display. Returns -1 if any of BCD
	// conversions is invalid (returns more than 9)
	int getMeasuredValue(void) {
		int result = 0;
		uint8_t digit0 = 0, digit1 = 0, digit2 = 0, digit3 = 0;
		// Read digits
		for (uint8_t i = 0; i < 4; i++) {
			digit0 |= digitalRead(Pins::digit0_pins[i]) << i;
			digit1 |= digitalRead(Pins::digit1_pins[i]) << i;
			digit2 |= digitalRead(Pins::digit2_pins[i]) << i;
			digit3 |= digitalRead(Pins::digit3_pins[i]) << i;
		}
		if (digit0 > 10) return (int) Pins::error_type::DIGIT0_NOT_BCD;
		if (digit1 > 10) return (int) Pins::error_type::DIGIT1_NOT_BCD;
		if (digit2 > 10) return (int) Pins::error_type::DIGIT2_NOT_BCD;
		if (digit3 > 10) return (int) Pins::error_type::DIGIT3_NOT_BCD;

		result = BCDToDecimal(digit0)
				+ 10 * BCDToDecimal(digit1)
				+ 100 * BCDToDecimal(digit2)
				+ 1000 * BCDToDecimal(digit3)
				+ 10000 * digitalRead(PIN_DIGIT4_0);

		return result;
	}

	Pins::measurement_range getMeasurementRange(void) {
		uint8_t range = 0;
		range |= digitalRead(PIN_RANGE_A) << 0;
		range |= digitalRead(PIN_RANGE_B) << 1;
		range |= digitalRead(PIN_RANGE_C) << 2;
		range |= digitalRead(PIN_OVERRANGE) << 3;
		return Pins::range_from_bits[range];
	}

	Pins::measurement_type getMeasurementType(void) {
		uint8_t type = 0;
		type |= digitalRead(PIN_AC_MEASURE) << 0;
		type |= digitalRead(PIN_DC_MEASURE) << 1;
		return Pins::type_from_bits[type];
	}

	Pins::measurement_sign getMeasurementSign(void) {
		uint8_t sign = 0;
		sign |= digitalRead(PIN_MEASURE_PLUS) << 0;
		sign |= digitalRead(PIN_MEASURE_MINUS) << 1;
		return Pins::sign_from_bits[sign];
	}


	// XXX: Shouldn't work since negative pulse is needed
	void startForcedMeasure(void) {
		digitalWrite(PIN_START_MEASURE, HIGH);
		delay(2);
		digitalWrite(PIN_START_MEASURE, LOW);
	}

	void stopMeasure(void) {
		digitalWrite(PIN_STOP_MEASURE, HIGH);
		delay(15);
		digitalWrite(PIN_STOP_MEASURE, LOW);
	}

	void blockMeasure(bool block) {
		if (block) {
			digitalWrite(PIN_BLOCK_MEASURE, LOW);
		} else {
			digitalWrite(PIN_BLOCK_MEASURE, HIGH);
		}
	}

}
