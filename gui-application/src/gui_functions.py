from tkinter import RAISED, SUNKEN, ACTIVE, DISABLED
from tkinter.filedialog import asksaveasfile 

def holdButtonCallback(self):
    self.hold.set(not self.hold.get()) #Toggle hold status
    if self.hold.get():
        self.display.config(bg ="#003b59")
    else:
        self.display.config(bg ="#1979a9")
        
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
    
def startSavingCallback(self):
    if not self.file:
        self.showInfo("Nie wybrano pliku do zapisu")
        return
    
    self.start_saving.state(['pressed', 'disabled'])
    self.stop_saving.state(['!pressed', '!disabled'])
    
def stopSavingCallback(self):
    self.start_saving.state(['!pressed', '!disabled'])
    self.stop_saving.state(['pressed', 'disabled'])
    self.file.close()

