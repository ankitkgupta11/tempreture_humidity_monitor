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

# ... (all your existing imports and functions)

def create_file_menu():
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New File", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=close_window)
    return file_menu

def create_edit_menu():
    edit_menu = Menu(menu_bar, tearoff=0)
    # Add Edit menu options here
    return edit_menu

def slave_setting():
    slave_menu = Menu(menu_bar, tearoff=0)
    # Add Edit menu options here
    return slave_menu

def new_file():
    messagebox.showinfo("New File", "Create a new file...")





def close_window():
    result = messagebox.askquestion("Close", "Are you sure you want to close?")
    if result == "yes":
        root.destroy()



connected = False  # Variable to keep track of the connection state

# Function to get the selected COM port
def toggle_connection():
    global connected  # Use the global keyword to access the global variable
    global selected_com
    global selected_file
    global selected_option

    selected_com = selected_com_var.get()


    
    if not selected_com:  # Check if a COM port is selected
        messagebox.showerror("Error", "Please select a COM port.")
        
        return
    
    try:
        if not connected:
            # Open the selected COM port
            ser = serial.Serial(port=selected_com, baudrate=115200, timeout=1)  # Update baudrate and timeout as needed
            ser.close()  # Close the port to release it from other applications
            ser.open()  # Reopen the port for communication
            

            # Add your serial communication code here
            
            message_var.set("Connected to COM Port: " + selected_com)  # Show connected message
            connect_button.config(text="Disconnect")
            connected = True

            # Start a thread for continuous reading
            start_continuous_reading_thread()

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

root = tk.Tk()
root.title("Deep Electronics")
root.geometry("1251x451")
root.protocol("WM_DELETE_WINDOW", close_window)

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

# Create a variable to store the selected COM port
selected_com_var = tk.StringVar(root)

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

#-----------------------------------------------//
def create_circle(canvas, color):
    canvas.create_oval(4, 4, 20, 20, fill=color, outline="black")

# Create a frame for valve data
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create lists to store start time and on duration values for each valve
start_time_vars = []
on_duration_vars = []

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

        # Create 2 text entry boxes for each valve: Start Time and On Duration
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
            start_time_label = tk.Label(valve_frame, text="Tempreture:", font=("Helvetica", 14))
            start_time_label.grid(row=2, column=1)
            start_time_var = tk.StringVar()  # Variable to store the value of Start Time
            start_time_entry = tk.Entry(valve_frame, width=10, font=("Helvetica", 14), textvariable=start_time_var,state="readonly")  # Limit the entry box to 10 characters
            start_time_entry.grid(row=2, column=2)
            start_time_vars.append(start_time_var)  # Append to the start time list
            # Set default values for the StringVar variables
            start_time_var.set("0")

            # Add canvas for temperature and humi
            canvas_humidity = tk.Canvas(valve_frame, width=20, height=20, bg="white")
            canvas_humidity.grid(row=3, column=0, padx=(10, 0), pady=5)  # Adjusted padding to give space

            on_duration_label = tk.Label(valve_frame, text="Humidity:", font=("Helvetica", 14))
            on_duration_label.grid(row=3, column=1)          
            create_circle(canvas_humidity, "green")  # Creating humidity circle
            on_duration_var = tk.StringVar()  # Variable to store the value of On Duration
            on_duration_entry = tk.Entry(valve_frame, width=10, font=("Helvetica", 14), textvariable=on_duration_var,state="readonly")  # Limit the entry box to 10 characters
            on_duration_entry.grid(row=3, column=2)
            on_duration_vars.append(on_duration_var)  # Append to the on duration list
            # Set default values for the StringVar variables
            on_duration_var.set("0")

            # Append the values of start_time_var and on_duration_var to the list
            valve_data.append(start_time_var)
            valve_data.append(on_duration_var)

            
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
            start_time_entry.config(validate="key", validatecommand=(vcmd, start_time_var, "%P"))
            on_duration_entry.config(validate="key", validatecommand=(vcmd, on_duration_var, "%P"))




# Function to start a thread for continuous reading
def start_continuous_reading_thread():
    threading.Thread(target=continuous_reading_thread).start()

# Function to perform continuous reading in a separate thread
def continuous_reading_thread():
    while connected:
        read_valve_data()
        time.sleep(2)  # Adjust the interval (in seconds) as needed
    # Function to read valve data from Modbus device


def read_valve_data():
        if not selected_com_var.get():
            messagebox.showerror("Error", "COM port is not selected.")
            return
        elif selected_com is None:
            messagebox.showerror("Error", "COM port is not selected.")
            return

        global valve_data_to_write

        try:
            # Send a read query to the Modbus device and update valve data if read is successful
            values_read = send_read_query_to_modbus(selected_com)
            if values_read is not None:
                valve_data_to_write = values_read
                update_gui_with_valve_data()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading data: {e}")


def update_gui_with_valve_data():
        global valve_data_to_write

        for i in range(8):  # Update the GUI elements with the received data
            start_time_var = start_time_vars[i]  # Accessing the start time variable for the current valve
            on_duration_var = on_duration_vars[i]  # Accessing the on duration variable for the current valve

            # Set the GUI variables with the received valve data
            start_time_var.set(str(valve_data_to_write[i * 2])) # Update start time for current valve
            on_duration_var.set(str(valve_data_to_write[i * 2 + 1]))  # Update on duration for current valve

def send_read_query_to_modbus(selected_com):
        ser = serial.Serial(port=selected_com, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        master = modbus_rtu.RtuMaster(ser)
        master.set_timeout(5.0)
        master.set_verbose(True)

        try:
            # Execute Modbus read query to get valve data
            values_read = master.execute(10, cst.READ_HOLDING_REGISTERS, 0, 22)  
            return values_read # Return the received valve data

        except modbus_tk.modbus.ModbusError as exc:
            messagebox.showerror("Modbus Error", f"Modbus error occurred: {exc}")
        finally:
            ser.close()
            master.close()



def save_file():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Writing the data rows
                for i in range(8):
                    temperature = start_time_vars[i].get()
                    humidity = on_duration_vars[i].get()
                    row = [temperature, humidity]
                    writer.writerow(row)
            messagebox.showinfo("Save File", f"Data saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving the file: {e}")



def open_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                # Skip header row
                for i, row in enumerate(csv_reader):
                    temperature, humidity = row
                    start_time_vars[i].set(temperature)
                    on_duration_vars[i].set(humidity)
            messagebox.showinfo("Open File", f"Data loaded from {file_path}")
    except Exception as e:
        messagebox.showerror("Open Error", f"An error occurred while opening the file: {e}")




menu_bar = Menu(root)
file_menu = create_file_menu()
edit_menu = create_edit_menu()
slave_menu=slave_setting()

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Slave Setting", menu=slave_menu)

root.config(menu=menu_bar)

root.mainloop()
