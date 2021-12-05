import tkinter as tk
from tkinter import RIGHT, LEFT, BOTH, RAISED, Label, X, messagebox
from tkinter.ttk import Frame, Button, Style, Combobox, Entry # For combobox widget
from tkinter.font import Font


class Application(tk.Frame):
    # Import the rest of class methods
    from serial_communication import serialPortsList, openPort, closePort, updatePorts, selectPort
    from receiver import receiveTask, initSerialBuffer, decodePacket
    from gui_functions import holdButtonCallback, voltageButtonCallback, currentButtonCallback, \
            saveButtonCallback, startSavingCallback, stopSavingCallback

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.measurement = tk.StringVar()
        self.measurement.set("0.0000 DC") # Default value
        self.measurement_mode = tk.StringVar()
        self.measurement_mode.set("V") # Can be Volts or Amperes
        self.hold = tk.BooleanVar() # HOLD menu option
        self.hold.set(False)
        self.port = tk.StringVar()
        self.serial = None
        self.file = None
        self.serial_baudrate = 115200
        self.pack()
        self.createWidgets()

    def showInfo(self, message):
        messagebox.showinfo("Miernik", message)
        
    def createWidgets(self):
        # Place for creating widgets
        self.master.title("Miernik")
        self.pack(fill=BOTH, expand=1)

        #display
        self.frame = Frame(self, relief=RAISED, borderwidth=1, width=100, height=100)
        self.frame.pack(fill=BOTH, expand=True)

        self.display = Label(self, fg="black", font=Font(family="Arial", size=40, weight = "bold"), bg ="#1979a9")
        self.display["textvariable"] = self.measurement
        self.display.place(width=400, height=160)

        self.ports_choice = Label(self, fg="black", font=Font(family="Arial", size=12, weight = "bold"))
        self.ports_choice["text"] = "Wybór portu"
        self.ports_choice.place(x=150, y =170)

        self.shunt_range = Label(self, fg="black", font=Font(family="Arial", size=7, weight="bold"))
        self.shunt_range["text"] = "Prąd znamionowy bocznika (A)"
        self.shunt_range.place(x=20, y=240)

        self.shunt_voltage = Label(self, fg="black", font=Font(family="Arial", size=7, weight="bold"))
        self.shunt_voltage["text"] = "Znamionowy spadek napięcia bocznika (mV)"
        self.shunt_voltage.place(x=20, y=290)

        self.frequency_choice = Label(self, fg="black", font=Font(family="Arial", size=7, weight="bold"))
        self.frequency_choice["text"] = "Częstotliwość zapisu wyników"
        self.frequency_choice.place(x=233, y=240)

        #buttons
        self.voltage_button = Button(self, text="Napięcie",style="SunkableButton.TButton", command = self.voltageButtonCallback)
        self.voltage_button.place(x=20, y=170)

        self.current_button = Button(self, text="Natężenie",style="SunkableButton.TButton", command = self.currentButtonCallback)
        self.current_button.state(['pressed', 'disabled'])
        self.current_button.place(x=20, y=200)
        
        self.stop_button = Button(self, text="HOLD", command = self.holdButtonCallback)
        self.stop_button.place(x=20, y=350)

        self.folder_button = Button(self, text="Folder zapisu", command = self.saveButtonCallback)
        self.folder_button.place(x=300, y=350)

        self.closeButton = Button(self, text="Otwórz port", command = self.openPort)
        self.closeButton.place(x=300, y=170)

        self.save_button = Button(self, text="Zamknij port", command = self.closePort)
        self.save_button.place(x=300, y=200)

        self.start_saving = Button(self, text="Start zapisu", command = self.startSavingCallback)
        self.start_saving.place(x=300, y=290)

        self.stop_saving = Button(self, text="Stop zapisu", command = self.stopSavingCallback)
        self.stop_saving.state(['pressed', 'disabled'])
        self.stop_saving.place(x=300, y=320)

        self.com_ports_list = Combobox(self, values=self.serialPortsList(), postcommand=self.updatePorts)
        self.com_ports_list.place(x=130, y=200)
        self.com_ports_list.bind('<<ComboboxSelected>>', self.selectPort)

        self.shunt_range_list = Combobox(self, values = [5, 10, 15, 20, 25, 50, 75, 100])
        self.shunt_range_list.place(x=20, y=260)

        self.shunt_voltage_list = Combobox(self, values=[30, 45, 60, 75, 100])
        self.shunt_voltage_list.place(x=20, y=310)

        self.save_options = Combobox(self, values=["1", "2"])  #temporary name #save frequency
        self.save_options.place(x=233, y=260)


root = tk.Tk()
app = Application(master=root)
root.geometry("400x400")
app.mainloop()
