import serial as serial

range_dict = {}
type_dict = {}
sign_dict = {}
range_dict["A"] = 0.00001
range_dict["B"] = 0.0001
range_dict["C"] = 0.001
range_dict["D"] = 0.01
range_dict["E"] = 0.1
range_dict["G"] = "Digit 0 is not BCD"
range_dict["H"] = "Digit 1 is not BCD"
range_dict["I"] = "Digit 2 is not BCD"
range_dict["J"] = "Digit 3 is not BCD"
range_dict["K"] = "Range pins configuration invalid"
range_dict["L"] = "Measurement type pins configuration invalid"
range_dict["M"] = "Sign pins configuration invalid"
range_dict["O"] = "Measurement out of range"

type_dict["A"] = "AC"
type_dict["D"] = "DC"
sign_dict["P"] = 1
sign_dict["M"] = -1


def decodePacket(self):
    # Decode packet
    measured_range = 1
    measured_type = ""
    measured_sign = 1
    measurement_result = 0

    try:
        if type(range_dict[self.serial_buffer[1]]) is float:
            measured_range = range_dict[self.serial_buffer[1]]
            #Signal overload in application
        elif self.serial_buffer[1] == "O":
            self.measurement.set('Overload!')
            return
        else:
            # Probably some transmission error
            return          

        measured_type = type_dict[self.serial_buffer[2]]
        measured_sign = sign_dict[self.serial_buffer[3]]
        
        measurement_result += int(self.serial_buffer[4]) * 10000 
        measurement_result += int(self.serial_buffer[5]) * 1000
        measurement_result += int(self.serial_buffer[6]) * 100 
        measurement_result += int(self.serial_buffer[7]) * 10
        measurement_result += int(self.serial_buffer[8]) * 1
        measurement_result *= measured_sign
        measurement_result *= measured_range
        # Voltage mode - round to prevent floating-point noise and return result
        if self.measurement_mode.get() == "V":
            self.raw_measurement = measurement_result
            # Offset for REL function
            measurement_result -= self.measurement_offset
            
            if abs(measurement_result) < 1.0:
                self.measurement.set(str(round(measurement_result*1000, 3)) + " mV " + measured_type)
            else:
                self.measurement.set(str(round(measurement_result, 3)) + " V " + measured_type)
        else:
            try:
                if measured_range != 0.00001:
                    self.measurement.set("Ustaw zakres \n 100mV")
                else:
                    # Calculate result according to Ohm's Law
                    measured_current = (measurement_result/((int(self.shunt_voltage_list.get())) * 0.001)) \
                        * int(self.shunt_range_list.get())
                    self.raw_measurement = measured_current
                    # Offset for REL function
                    measured_current -= self.measurement_offset

                    if measured_current > 1.2 * int(self.shunt_range_list.get()):
                        self.measurement.set('Overload!')
                    else:
                        if abs(measured_current) < 1.0:
                            self.measurement.set(str(round(measured_current*1000, 3)) + " mA " + measured_type)
                        else:
                            self.measurement.set(str(round(measured_current, 3)) + " A " + measured_type)
            except:
                return
        # For debugging purposes
        #print(self.measurement.get())
    except KeyError:
        print("Invalid frame")

def initSerialBuffer(self):
    self.serial_buffer = [None] * 11
    self.synced = False
    self.packet_pos = 0

def receiveTask(self):
    #Read buffer and update measured fields
    while True:
        if not self.serial:
            break
        inputByte = self.serial.read()
        if not inputByte:
            break
        # convert byte to character
        try:
            c = inputByte.decode("ascii")
        except(UnicodeDecodeError):
            print("Transmission error")
            break
        if (self.synced and c != '$'):
            continue;

        # We have '$' on input - sync packet
        synced = True

        # Add characters to buffer
        if (self.packet_pos > 0 or c == '$'):
            self.serial_buffer[self.packet_pos] = c
            self.packet_pos = self.packet_pos + 1 
            #Check if the end of the packet is correct
            if (self.packet_pos == 10 and self.serial_buffer[9] != '\r'
                or self.packet_pos == 11 and self.serial_buffer[10] != '\n'):
                # Packet invalid - start synchronizing again
                self.packet_pos = 0
                self.synced = False
            # Packet seems to be correct
            elif (self.packet_pos == 11):
                #fill the packet
                self.packet_pos = 0
                # Decode Packet only if HOLD isn't on
                if not self.hold.get():
                    self.decodePacket()
    #Run every 100 ms
    self.master.after(100, self.receiveTask)
