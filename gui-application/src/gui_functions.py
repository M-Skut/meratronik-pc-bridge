from tkinter import RAISED, SUNKEN, ACTIVE, DISABLED
from tkinter.filedialog import asksaveasfile, asksaveasfilename
import datetime
import sqlite3 as sqlite


# Is HOLD on, is REL on defines background color
measurement_backgrounds = {
    (False, False): "#1979a9",
    (True, False): "#156a94",
    (False, True): "#228b22",
    (True, True): "#256925",
    }

def holdButtonCallback(self):
    self.hold.set(not self.hold.get()) #Toggle hold status
    self.display.config(bg = measurement_backgrounds[(self.hold.get(),self.rel.get())])
    
def relButtonCallback(self):
    self.rel.set(not self.rel.get()) #Toggle rel status
    if self.rel.get():
        self.measurement_offset = self.raw_measurement
    else:
        self.measurement_offset = 0.00
    self.display.config(bg = measurement_backgrounds[(self.hold.get(),self.rel.get())])
    
def voltageButtonCallback(self):
    self.voltage_button.state(['pressed', 'disabled'])
    self.current_button.state(['!pressed', '!disabled'])
    self.measurement_mode.set("V")
    
def currentButtonCallback(self):
    self.voltage_button.state(['!pressed', '!disabled'])
    self.current_button.state(['pressed', 'disabled'])
    self.measurement_mode.set("A")
    
def saveButtonCallback(self):
    self.file = asksaveasfile(mode='w', defaultextension=".csv")
    self.database = asksaveasfilename(defaultextension=".db")

def periodicSave(self):
    if (self.flag_point == 1):
        # CSV part
        dynamic_parameter = float(self.save_options.get())
        current_time = datetime.datetime.now()
        current_data = self.measurement.get()
        current_data = current_data.replace(" ", ",")
        temporary_counter = str(self.counter)
        temporary_time = current_time.strftime("%H:%M:%S:%d.%m.%Y")
        self.file.writelines(temporary_counter+','+temporary_time+','+current_data+"\n")
        self.counter += 1
        delay = int(1000/dynamic_parameter)

        # Database part
        try:
            conn = sqlite.connect(self.database)
        except IOError as e:
            pass
        with conn:
            voltage, current = 0, 0
            if self.measurement_mode.get() == "V":
                voltage = self.raw_measurement
            else:
                current = self.raw_measurement
                
            conn = conn.cursor()
            conn.execute(
                "INSERT INTO meratronik_data VALUES(datetime('now', 'localtime'), (?), (?))", (voltage, current))

        self.master.after(delay, self.periodicSave)
    else:
        self.file.close()
    
def startSavingCallback(self):
    if not self.file:
        self.showInfo("Nie wybrano pliku do zapisu")
        return
    if not self.save_options.get():
        self.showInfo("Nie wybrano częstotliwości zapisu")
        return
    self.flag_point = 1
    self.counter = 1
    self.file.write('Format zapisu danych:'+"\n")
    self.file.write('Numer pomiaru, data wykonania pomiaru, wartość pomiaru, wielkość mierzona'+"\n")

    #If no db file selected, ignore saving to it, else create it with correct schema
    if self.database:
        conn = sqlite.connect(self.database)
        with conn:
            conn = conn.cursor()
            conn.execute(
                "CREATE TABLE meratronik_data(timestamp DATETIME, voltage NUMERIC, current NUMERIC)")
   
    periodicSave(self)
    self.start_saving.state(['pressed', 'disabled'])
    self.stop_saving.state(['!pressed', '!disabled'])

    
def stopSavingCallback(self):
    self.flag_point = 0
    self.start_saving.state(['!pressed', '!disabled'])
    self.stop_saving.state(['pressed', 'disabled'])