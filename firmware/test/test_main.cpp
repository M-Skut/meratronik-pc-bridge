#include <Arduino.h>
#include <stdint.h>
#include <unity.h>
#include <io_utils.h>

//TODO: Write more sane tests

void testBCD(){
	TEST_ASSERT_EQUAL(0, IOUtils::BCDToDecimal((uint8_t) 0b00000000));
	TEST_ASSERT_EQUAL(6, IOUtils::BCDToDecimal((uint8_t) 0b00000110));
	TEST_ASSERT_EQUAL(3, IOUtils::BCDToDecimal((uint8_t) 0b00000011));
	TEST_ASSERT_EQUAL(9, IOUtils::BCDToDecimal((uint8_t) 0b00001001));
}

void setup() {
	delay(3000); // Wait in case of USB enumeration problems
	UNITY_BEGIN();
	RUN_TEST(testBCD);
}

void loop() {
	UNITY_END();
}
