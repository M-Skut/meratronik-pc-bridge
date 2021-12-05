
import serial as serial
from serial.tools import list_ports


# Serial port class methods

def serialPortsList(self):
    return serial.tools.list_ports.comports()


def openPort(self):
    if not self.port.get(): 
        self.showInfo("Nie wybrano portu")
        return;
    if self.serial == None:
        self.serial = serial.Serial(port=self.port.get(), baudrate=self.serial_baudrate, timeout=0, writeTimeout=0)
    else:
        # Serial already opened - close it
        self.serial.close()
        self.serial = serial.Serial(port=self.port.get(), baudrate=self.serial_baudrate, timeout=0, writeTimeout=0)
    # Send start signal and Call receiver
    self.initSerialBuffer()
    self.serial.write(b'S')
    self.master.after(1000, self.receiveTask)
    
    
def closePort(self):
    if not self.serial: 
        self.showInfo("Nie otwarto portu")
        return;
    self.serial.close()
    self.serial = None
    
def updatePorts(self):
    port_list = serialPortsList(self)
    ports = [port.device for port in port_list]
    self.com_ports_list['values'] = ports
    
def selectPort(self, event=None):
    self.port.set(event.widget.get())