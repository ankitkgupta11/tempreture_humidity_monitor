import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import serial.tools.list_ports as list_ports
import time
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import threading
from datetime import datetime
from tkinter import *
import csv
from tkinter import filedialog
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Menu
from tkinter import simpledialog
import os
import json 
import tkinter.simpledialog

#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def create_file_menu():
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=close_window)
    return file_menu

def create_edit_menu():
    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Start Read", command=start_reading)

    edit_menu.add_command(label="Baud Rate", command=select_baud_rate)

    edit_menu.add_command(label="Enter Slave ID:", command=enter_slave_id)
    
    return edit_menu

#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Function to perform continuous reading in a separate thread
def start_reading():
    try:
        if not selected_com_var.get():
            raise ValueError("COM port is not selected. Please select a COM port.")

        if not connected:
            raise ValueError("Not connected to COM port. Please connect first.")

        # Start reading from Modbus (you can put your reading logic here)
        start_continuous_reading_thread()
        set_reading_status("Reading from Modbus...")

        messagebox.showinfo("Start Read", "Reading from Modbus has started.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_baud_rate():
    baud_rate_options = [9600, 4800]

    # Create a new window (Toplevel) for the dialog
    dialog = tk.Toplevel(root)
    dialog.title("Select Baud Rate")
    dialog.title("Select Baud Rate")

    # Add a heading label
    heading_label = ttk.Label(dialog, text="Select Baud Rate", font=("Helvetica", 14, "bold"))
    heading_label.pack(pady=10)

    # Create a Combobox for selecting baud rates
    selected_baud_rate_value = tk.StringVar()
    selected_baud_rate_value.set(selected_baud_rate.get())  # Set the default value

    baud_rate_combobox = ttk.Combobox(dialog, textvariable=selected_baud_rate_value, values=baud_rate_options, state="readonly")
    baud_rate_combobox.pack(padx=20, pady=10)

    # Function to handle the OK button click
    def on_ok():
        selected_baud_rate.set(selected_baud_rate_value.get())
        dialog.destroy()

    # Create an OK button to confirm the selection
    ok_button = tk.Button(dialog, text="OK", command=on_ok)
    ok_button.pack(pady=10)

# ...



#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def close_window():
    result = messagebox.askquestion("Close", "Are you sure you want to close?")
    if result == "yes":
        root.destroy()

#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
CONFIG_FILE = "config.json"  

# Load configuration from file
def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
    return config

# Save configuration to file
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)


connected = False  # Variable to keep track of the connection state
global selected_baud_rate

# Function to get the selected COM port
def toggle_connection():
    global connected  # Use the global keyword to access the global variable
    global selected_com
    global selected_baud_rate
    global selected_slave_id

    selected_com = selected_com_var.get()
    selected_baud_rate_value = int(selected_baud_rate.get())
    selected_slave_id_value = selected_slave_id.get()


    if not selected_com:  # Check if a COM port is selected
        messagebox.showerror("Error", "Please select a COM port.")
        
        return
    
    try:
        if not connected:
            # Open the selected COM port
            ser = serial.Serial(port=selected_com, baudrate=int(selected_baud_rate_value), timeout=1)  # Update baudrate and timeout as needed
            ser.close()  # Close the port to release it from other applications
            ser.open()  # Reopen the port for communication
            
            # Update the configuration with the selected values
            # Update the configuration with the selected values
            config = load_config()
            config['com_port'] = selected_com
            config['baud_rate'] = int(selected_baud_rate_value)
            config['slave_id'] = int(selected_slave_id_value)
            save_config(config)
            # Add your serial communication code her
            
            # message_var.set("Connected to COM Port: " + selected_com)  # Show connected message
            message_var.set(f"Connected to COM Port: {selected_com}")

            connect_button.config(text="Disconnect")
            connected = True
            set_reading_status("Not Reading")


            # Start a thread for continuous reading
            #start_continuous_reading_thread()

        else:
            # Close the COM port
            selected_com = None  # Reset selected_com to None
            #selected_com_var.set("Select COM")  # Reset the dropdown to "Select COM"
            com_dropdown.set("Select COM")  # Set default option to "Select COM"
            # Add your serial communication code here

            
            message_var.set("Disconnected from COM Port")  # Show disconnected message
            connect_button.config(text="Connect")
            connected = False

            
    except serial.SerialException as e:
        messagebox.showerror("Connection Error", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

root = tk.Tk()
root.title("DeepEl_")
root.geometry("1251x451")
root.protocol("WM_DELETE_WINDOW", close_window)

#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Create a frame for title and COM port selection
title_frame = ttk.Frame(root)
title_frame.pack(pady=10)

# Create a title label in the middle
title_label = ttk.Label(title_frame, text="                                                  Tempreture and Humidity Monitor                                             ", background="blue", foreground="white", font=("Helvetica", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=4, padx=10)

# Get available COM ports
com_ports = list_ports.comports()
com_ports_list = [port.device for port in com_ports]

# Create a frame for COM port selection
com_frame = ttk.Frame(root)
com_frame.pack(pady=10)

# Create a label for COM port selection
com_label = ttk.Label(com_frame, text="Select COM Port:", font=("Helvetica", 14))
com_label.pack(side=tk.LEFT)

# Create a status bar
status_bar = tk.Label(root, text="Not Reading", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)


def set_reading_status(status):
    status_bar.config(text=status)
# Create a variable to store the selected COM port
selected_com_var = tk.StringVar(root)

selected_baud_rate = tk.StringVar(root)
selected_baud_rate.set("9600")  # Set default baud rate

selected_slave_id = tk.StringVar(root)
selected_slave_id.set("1")  # Set default slave ID

# Create a dropdown button for COM port selection
com_dropdown = ttk.Combobox(com_frame, textvariable=selected_com_var, values=com_ports_list, font=("Helvetica", 14), state="readonly")
com_dropdown.pack(side=tk.LEFT)

# Create a button to connect/disconnect from the COM port
connect_button = tk.Button(com_frame, text="Connect", command=toggle_connection, font=("Helvetica", 14))
connect_button.pack(side=tk.LEFT, padx=5)

# Create a separator line
separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X, padx=10, pady=5)

# Create a variable to store the connection status message
message_var = tk.StringVar(root)

# Create a label to display the connection status message
message_label = tk.Label(root, textvariable=message_var, font=("Helvetica", 14, "bold"))
message_label.pack()


#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#json saving
# Load configuration at the beginning
config = load_config()
selected_com_var.set(config.get('com_port', 'Select COM'))

# Convert baud rate and slave ID to integers
baud_rate_from_config = int(config.get('baud_rate', '9600'))
slave_id_from_config = int(config.get('slave_id', '1'))

selected_baud_rate.set(str(baud_rate_from_config))
selected_slave_id.set(str(slave_id_from_config))


#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def create_circle(canvas, color):
    canvas.create_oval(4, 4, 20, 20, fill=color, outline="black")

# Create a frame for valve data
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create lists to Tempreture and Humidity values for each valve
tempreture_vars = []
humidity_vars = []

# Create a list to store valve data
valve_data = []
valve_labels = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "6",
        6: "7",
        7: "8",
         }

        # Create 2 text entry boxes for each valve: Tempreture and Humidity
entry_boxes = []
for i in range(8): 
            valve_frame = ttk.Frame(frame)
            valve_frame.grid(row=i % 4, column=i // 4, padx=20, pady=10, sticky="nw")

            valve_frame = ttk.Frame(frame)
            col = i % 4+1
            row = i // 4
            valve_frame.grid(row=row, column=col, padx=20, pady=10, sticky="nw")

            valve_label = ttk.Label(valve_frame, text=valve_labels.get(i, "Valve " + str(i + 1)), font=("Helvetica", 14, "bold"))
            valve_label.grid(row=0, column=0, columnspan=2)

            separator_line = ttk.Separator(valve_frame, orient=tk.HORIZONTAL)
            separator_line.grid(row=1, column=0, columnspan=2, sticky="ew")

            # Add canvas for temperature and humidity indicators
            canvas_temp = tk.Canvas(valve_frame, width=20, height=20, bg="white")
            canvas_temp.grid(row=2, column=0, padx=(10, 0), pady=5)  # Adjusted padding to give space

            create_circle(canvas_temp, "red")  # Creating temperature circle
            tempreture_label = tk.Label(valve_frame, text="Tempreture:", font=("Helvetica", 14))
            tempreture_label.grid(row=2, column=1)
            tempreture_var = tk.StringVar()  # Variable to store the value of Tempreture
            tempreture_entry = tk.Entry(valve_frame, width=10, font=("Helvetica", 14), textvariable=tempreture_var,state="readonly")  # Limit the entry box to 10 characters
            tempreture_entry.grid(row=2, column=2)
            tempreture_vars.append(tempreture_var)  # Append to the tempreture list
            # Set default values for the StringVar variables
            tempreture_var.set("0")

            # Add canvas for temperature and humi
            canvas_humidity = tk.Canvas(valve_frame, width=20, height=20, bg="white")
            canvas_humidity.grid(row=3, column=0, padx=(10, 0), pady=5)  # Adjusted padding to give space

            humidity_label = tk.Label(valve_frame, text="Humidity:", font=("Helvetica", 14))
            humidity_label.grid(row=3, column=1)          
            create_circle(canvas_humidity, "green")  # Creating humidity circle
            humidity_var = tk.StringVar()  # Variable to store the value of On Duration
            humidity_entry = tk.Entry(valve_frame, width=10, font=("Helvetica", 14), textvariable=humidity_var,state="readonly")  # Limit the entry box to 10 characters
            humidity_entry.grid(row=3, column=2)
            humidity_vars.append(humidity_var)  # Append to the on duration list
            # Set default values for the StringVar variables
            humidity_var.set("0")

            # Append the values of tempreture_var and humidity_var to the list
            valve_data.append(tempreture_var)
            valve_data.append(humidity_var)

            
            # Function to validate and limit the input to numeric values only within the range of 1 to 65350
            def validate_numeric_input(var, new_value):
                if new_value == "":  # Allow empty input (deletion)
                    return True

                if new_value.isdigit():
                    value = int(new_value)
                    if 0 <= value <= 65350:
                        return True
                return False

            # Register the validation function to the entry boxes
            vcmd = root.register(validate_numeric_input)
            tempreture_entry.config(validate="key", validatecommand=(vcmd, tempreture_var, "%P"))
            humidity_entry.config(validate="key", validatecommand=(vcmd, humidity_var, "%P"))


#------------------------------------------------////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# function for starting the read from menu

# Function to start a thread for continuous reading
def start_continuous_reading_thread():
    threading.Thread(target=continuous_reading_thread).start()

def continuous_reading_thread():
    while connected:
        read_valve_data(selected_slave_id.get())
        time.sleep(4)  # Adjust the interval (in seconds) as needed
    set_reading_status("Not Reading")



#------------------------------------------------//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# function for sending valve data to modbus
def read_valve_data(selected_slave_id):
    if not selected_com_var.get():
        messagebox.showerror("Error", "COM port is not selected.")
        return
    elif selected_com is None:
        messagebox.showerror("Error", "COM port is not selected.")
        return

    global valve_data_to_write

    try:
        # Send a read query to the Modbus device and update valve data if read is successful
        values_read = send_read_query_to_modbus(selected_com, selected_slave_id)
        if values_read is not None:
            valve_data_to_write = values_read
            update_gui_with_valve_data()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading data: {e}")



def update_gui_with_valve_data():
        global valve_data_to_write

        for i in range(8):  # Update the GUI elements with the received data
            tempreture_var = tempreture_vars[i]  # Accessing the tempreture time variable for the current valve
            humidity_var = humidity_vars[i]  # Accessing the humidity variable for the current valve

            # Set the GUI variables with the received valve data
            tempreture_var.set(str(valve_data_to_write[i * 2])) # Update tempreture time for current valve
            humidity_var.set(str(valve_data_to_write[i * 2 + 1]))  # Update humidity for current valve

selected_baud_rate = tk.StringVar(root)
selected_baud_rate.set("9600")  # Set default baud rate
selected_baud_rate_value = selected_baud_rate.get()



def send_read_query_to_modbus(selected_com, selected_slave_id):
    ser = serial.Serial(port=selected_com, baudrate=int(selected_baud_rate_value), bytesize=8, parity='N', stopbits=1, xonxoff=0)
    master = modbus_rtu.RtuMaster(ser)
    master.set_timeout(5.0)
    master.set_verbose(True)

    try:
        # Execute Modbus read query to get valve data using the selected Slave ID
        values_read = master.execute(int(selected_slave_id), cst.READ_HOLDING_REGISTERS, 0, 22)
        return values_read  # Return the received valve data

    except modbus_tk.modbus.ModbusError as exc:
        messagebox.showerror("Modbus Error", f"Modbus error occurred: {exc}")
    finally:
        ser.close()
        master.close()

#------------------------------------------------//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# for save valve data to csv file
def save_file():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Writing the data rows
                for i in range(8):
                    temperature = tempreture_vars[i].get()
                    humidity = humidity_vars[i].get()
                    row = [temperature, humidity]
                    writer.writerow(row)
            messagebox.showinfo("Save File", f"Data saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving the file: {e}")


# For opening a csv file
def open_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                # Skip header row
                for i, row in enumerate(csv_reader):
                    temperature, humidity = row
                    tempreture_vars[i].set(temperature)
                    humidity_vars[i].set(humidity)
            messagebox.showinfo("Open File", f"Data loaded from {file_path}")
    except Exception as e:
        messagebox.showerror("Open Error", f"An error occurred while opening the file: {e}")

#------------------------------------------------//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def enter_slave_id():  
    # Create a simple dialog for entering the Slave ID
    slave_id_value = simpledialog.askinteger("Enter Slave ID", "Please enter the Slave ID (0-255):", initialvalue=int(selected_slave_id.get()), minvalue=0, maxvalue=255)
    
    if slave_id_value is not None:
        selected_slave_id.set(str(slave_id_value))

#------------------------------------------------//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# MENU OPTION
menu_bar = Menu(root)
edit_menu = create_edit_menu()
file_menu = create_file_menu()

menu_bar.add_cascade(label="Comm", menu=edit_menu)
menu_bar.add_cascade(label="Data", menu=file_menu)

root.config(menu=menu_bar)

#------------------------------------------------//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


root.mainloop()
