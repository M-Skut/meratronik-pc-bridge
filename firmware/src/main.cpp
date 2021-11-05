#include <Arduino.h>
#include <cstdio>
#include <io_utils.h>


char dataPacket[] = {'$', 'R', 'T', 'S', 1, 1, 1, 1, 1, '\r', '\n'};
// Packets to send when there is any error
// Error codes declared in document
// Rest of the packet does not matter and it's just to preserve format
static const char digit0_error_packet[] = "$GAP00000\r\n";
static const char digit1_error_packet[] = "$HAP00000\r\n";
static const char digit2_error_packet[] = "$IAP00000\r\n";
static const char digit3_error_packet[] = "$JAP00000\r\n";
static const char range_error_packet[] =  "$KAP00000\r\n";
static const char type_error_packet[] =   "$LAP00000\r\n";
static const char sign_error_packet[] =   "$MAP00000\r\n";


void setup() {
    IOUtils::initPins();
    Serial.begin(115200);
    Serial.println("Waiting for start");
    // Clear buffer
    while (Serial.available() && Serial.read());
    // Wait for signal
    while (!Serial.available());
    // Clear buffer again
    while (Serial.available() && Serial.read());
}

void loop() {
	int measurement = IOUtils::getMeasuredValue();
	Pins::measurement_range range = IOUtils::getMeasurementRange();
	Pins::measurement_type type = IOUtils::getMeasurementType();
	Pins::measurement_sign sign = IOUtils::getMeasurementSign();

	// Check for errors and send pre-made error packets in case of one
	if (measurement < 0) {

		if (measurement == Pins::error_type::DIGIT0_NOT_BCD) {
			Serial.write(digit0_error_packet);
		} else if (measurement == Pins::error_type::DIGIT1_NOT_BCD) {
			Serial.write(digit1_error_packet);
		} else if (measurement == Pins::error_type::DIGIT2_NOT_BCD) {
			Serial.write(digit2_error_packet);
		} else {
			Serial.write(digit3_error_packet);
		}
	} else if (range == Pins::measurement_range::RANGE_UNDEFINED) {
		Serial.write(range_error_packet);
	} else if (type == Pins::measurement_type::TYPE_UNDEFINED) {
		Serial.write(type_error_packet);
	} else if (sign == Pins::measurement_sign::SIGN_UNDEFINED) {
		Serial.write(sign_error_packet);
	} else {
		char rangeData = Pins::range_to_char[range];
		char typeData = Pins::type_to_char[type];
		char signData = Pins::sign_to_char[sign];

		// Construct packet
		dataPacket[1] = rangeData;
		dataPacket[2] = typeData;
		dataPacket[3] = signData;

		dataPacket[8] = measurement % 10 + '0';
		measurement /= 10;
		dataPacket[7] = measurement % 10 + '0';
		measurement /= 10;
		dataPacket[6] = measurement % 10 + '0';
		measurement /= 10;
		dataPacket[5] = measurement % 10 + '0';
		measurement /= 10;
		dataPacket[4] = measurement % 10 + '0';
		Serial.print(dataPacket);
	}
	// TODO: Control measurement
	delay (1000); // To be removed in release

}
