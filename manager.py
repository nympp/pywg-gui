######################################################
# python/tkinter Wireguard Connections Manager       #
# Git : https://github.com/nympp/py-vpnmanager       #
######################################################

# CHANGE THIS :
MANAGER_INSTALL_PATH = "/home/phileas/Documents/Git/py-vpnmanager" # "~/Documents/pywg-gui"
BASE_OPEN_PATH = "/home/phileas/Téléchargements"

# Libraries import

# TkInter, GUI
from tkinter import *
from tkinter import filedialog

# CSV, to read CSV files
import csv

import os
import subprocess

# Functions

def ac_select_file():
    global file, ac_popup_tk, enter_filename, enter_prettyfilename

    # To select the wireguard config file, opens where you set to in the config file, default is /home
    file = filedialog.askopenfilename(initialdir=f"{BASE_OPEN_PATH}", filetypes=(("Wireguard Conf Files", "*.conf"), ("All files", "*.*")))

    showfile = Label(ac_popup_tk, text=f"File selected : {file}")
    showfile.pack()


    Label(ac_popup_tk, text="Enter the file name (avoid '*', '/', '.', ':') :").pack()
    enter_filename = Text(ac_popup_tk, height=1, width=20)
    enter_filename.pack()

    Label(ac_popup_tk, text="Enter the pretty file name (the one that will be displayed on the manager) :").pack()
    enter_prettyfilename = Text(ac_popup_tk, height=1, width=20)
    enter_prettyfilename.pack()

    Button(ac_popup_tk, text="Add connection", command=add_connection_to_wg).pack()


def add_connection():
    global ac_popup_tk

    ac_popup_tk = Tk()
    ac_popup_tk.geometry(f"{600}x{600}")
    ac_popup_tk.title("Add a new Wireguard connection")

    select_file_button = Button(ac_popup_tk, text="Select .conf file", command=ac_select_file)
    select_file_button.pack()
    

    ac_popup_tk.mainloop()

def add_connection_to_wg():
    global enter_prettyfilename, enter_filename, file

    prettyfilename = enter_prettyfilename.get("1.0", "end-1c")
    filename = enter_filename.get("1.0", "end-1c")

    # print(filename, prettyfilename)

    # Moving the selected config file to /etc/wireguard and adding to the connections.csv
    subprocess.run(["sudo", "cp", file, f"/etc/wireguard/{filename}.conf"])

    datarow = [prettyfilename, filename]

    with open(f"{MANAGER_INSTALL_PATH}/config/connections.csv", "a", newline="") as connections:
        f_csv = csv.writer(connections, delimiter=",")
        f_csv.writerow(datarow)

    # Once completed, kill the window
    ac_popup_tk.destroy()

# Main program

print("Elevating with sudo...")
subprocess.run(["sudo", "echo", "Done!"])

# Setting up the window
root_tk = Tk() # base Tk, named root_tk
root_tk.geometry(f"{800}x{870}") # window size
root_tk.title("Wireguard Connections Manager")

main_title = Label(root_tk, text="Wireguard Connection Manager")
main_title.pack()

# "add a connection" part

add_button = Button(root_tk, text="Add a Wireguard Connection", command=add_connection)
add_button.pack()

# Available conncetions display

data = []

with open("{MANAGER_INSTALL_PATH}/config/connections.csv", newline="") as connections:
    reader = csv.DictReader(connections, delimiter=",")
    for row in reader:
        data.append(row)

for row in data:
    l = Label(root_tk, text=f"{row["vpn_pretty_name"]}")
    l.pack()




# subprocess.run(["sudo","ls","/etc/wireguard"]) 

# Textbox, can be used for the pretty name of the connection
# textbox = Text(root_tk, height=10, width=40)
# textbox.pack()

root_tk.mainloop()