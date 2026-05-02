################################################
# python/tkinter Wireguard Connections Manager #
# Git : https://github.com/nympp/pywg-gui      #
################################################

# CHANGE THIS :
MANAGER_INSTALL_PATH = "/home/phileas/Documents/Git/pywg-gui" #"~/Documents/pywg-gui"
BASE_OPEN_PATH = "/home/phileas/Téléchargements"

# Libraries import

# TkInter, GUI
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

# CSV, to read CSV files
import csv

import os
import subprocess

# Functions

def ac_select_file():
    global file, ac_popup_tk, enter_filename, enter_prettyfilename

    # TODO : Redo this with .place() instead of .pack() for elements, for a better look

    # To select the wireguard config file, opens where you set to in the config file, default is /home
    file = filedialog.askopenfilename(initialdir=f"{BASE_OPEN_PATH}", filetypes=(("Wireguard Conf Files", "*.conf"), ("All files", "*.*")))

    # The label that shows which file has been selected
    showfile = Label(ac_popup_tk, text=f"File selected : {file}", bg="#1e1e1e", fg="white")
    showfile.pack()

    # Label & Text zone for the filename that will be used by wireguard (will be save as FILENAME.conf)
    Label(ac_popup_tk, text="Enter the file name (avoid '*', '/', '.', ':') :", bg="#1e1e1e", fg="white").pack()
    enter_filename = Text(ac_popup_tk, height=1, width=20, fg="white", bg="#464646")
    enter_filename.pack()

    # Label & Text zone for the "Pretty Filename", which means the name that will be displayed on pyWG-GUI
    Label(ac_popup_tk, text="Enter the pretty file name (the one that will be displayed on the manager) :", bg="#1e1e1e", fg="white").pack()
    enter_prettyfilename = Text(ac_popup_tk, height=1, width=20, fg="white", bg="#464646")
    enter_prettyfilename.pack()

    # The button to add the connection
    Button(ac_popup_tk, text="Add connection", command=add_connection_to_wg, fg="white", bg="#464646").pack()


def add_connection():
    global ac_popup_tk

    # First, when loading a new popup of the root_tk, delete all other potential popups on screen
    kill_popups()

    ac_popup_tk = Toplevel() # TopLevel() instead of Tk()
    ac_popup_tk.geometry(f"{600}x{600}")
    ac_popup_tk.title("Add a new Wireguard connection")
    ac_popup_tk.configure(bg="#1e1e1e") # Dark gray/black background

    # The button to launch the select file & renaming function (ac_select_file())
    select_file_button = Button(ac_popup_tk, text="Select .conf file", command=ac_select_file, fg="white", bg="#464646")
    select_file_button.pack()

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

    # Reload the list once a new connection is added
    display_all_connections_available()

    # Once completed, kill the window
    ac_popup_tk.destroy()

def display_all_connections_available():
    global root_tk

    data = []

    with open(f"{MANAGER_INSTALL_PATH}/config/connections.csv", newline="") as connections:
        reader = csv.DictReader(connections, delimiter=",")
        for row in reader:
            data.append(row)

    h = 145

    for row in data:
        filename = row["file_name"]
        prettyname = row["vpn_pretty_name"]

        Canvas(
            root_tk,
            width=780,
            height=50,
            bg="#464646"
        ).place(x=10, y=h)

        Label(root_tk, text=f"{prettyname}", fg="white", bg="#464646").place(x=20, y=h+12)

        Button(root_tk, text="Connect", command=lambda f=filename: connect(f), fg="white", bg="#1B1B1B").place(x=575, y=h+7)
        Button(root_tk, text="Disconnect", command=disconnect_interfaces, fg="white", bg="#1B1B1B").place(x=670, y=h+7)

        h += 50

def connect(interface :str):

    subprocess.run(
        ["sudo", "wg-quick", "up", interface]
    )

    print(f"Connected to {interface}!")

def disconnect_interfaces():
    subprocess.run("sudo wg show interfaces | xargs -n1 sudo wg-quick down", shell=True, check=True)

    # for row in data:
    #    l = Label(root_tk, text=f"{row["vpn_pretty_name"]}")
    #    l.pack()

    # disconnect all : sudo wg show interfaces | xargs -n1 sudo wg-quick down

def quit():
    global root_tk

    root_tk.destroy()

    print("Exited succesfully.")

def manage_connections():
    global mc_popup_tk

    kill_popups()

    mc_popup_tk = Toplevel()
    mc_popup_tk.geometry(f"{600}x{600}")
    mc_popup_tk.title("Manage connections")
    mc_popup_tk.configure(bg="#1e1e1e")

    Label(mc_popup_tk, text="Manage Wireguard connections", fg="white", bg="#1e1e1e").place(x=10, y=10)
    Button(mc_popup_tk, text="Refresh list", fg="white", bg="#464646", command=display_all_connections_available_mc).place(x=480, y=5)

    display_all_connections_available_mc()

    Button(mc_popup_tk, text="Quit", fg="white", bg="#464646", command=quit_mc).place(x=530, y=555)

def quit_mc():
    global mc_popup_tk
    mc_popup_tk.destroy()

def display_all_connections_available_mc():
    global mc_popup_tk

    data = []

    with open(f"{MANAGER_INSTALL_PATH}/config/connections.csv", newline="") as connections:
        reader = csv.DictReader(connections, delimiter=",")
        for row in reader:
            data.append(row)

    h = 45

    for row in data:
        filename = row["file_name"]
        prettyname = row["vpn_pretty_name"]

        Canvas(
            mc_popup_tk,
            width=580,
            height=50,
            bg="#464646"
        ).place(x=10, y=h)

        Label(mc_popup_tk, text=f"{prettyname}", fg="white", bg="#464646").place(x=20, y=h+12)

        Button(mc_popup_tk, text="Rename", command=lambda f=filename, p=prettyname: rename_popup(f,p), fg="white", bg="#1B1B1B").place(x=412, y=h+7)
        Button(mc_popup_tk, text="Delete", command=disconnect_interfaces, fg="white", bg="#1B1B1B").place(x=508, y=h+7)

        h += 50

def rename_connection(filename: str):
    global new_prettyname_input, rename_mc_popup_tk

    new_pretty_name = new_prettyname_input.get("1.0", "end-1c")
    
    data = []

    with open(f"{MANAGER_INSTALL_PATH}/config/connections.csv", newline="") as connections:
        reader = csv.DictReader(connections, delimiter=",")

        for row in reader:
            if row["file_name"] == filename:
                row["vpn_pretty_name"] = new_pretty_name
            data.append(row)

    with open(f"{MANAGER_INSTALL_PATH}/config/connections.csv", "w", newline="") as connections:
        writer = csv.DictWriter(connections, delimiter=",", fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    display_all_connections_available()
    display_all_connections_available_mc()
    rename_mc_popup_tk.destroy()
                                                                                                                  
def rename_popup(filename: str, current_pretty_name: str):
    global rename_mc_popup_tk, new_prettyname_input

    rename_mc_popup_tk = Toplevel()
    rename_mc_popup_tk.geometry(f"{400}x{75}")
    rename_mc_popup_tk.title("Rename prompt")
    rename_mc_popup_tk.configure(bg="#1e1e1e")

    Label(rename_mc_popup_tk, text=f"Rename {current_pretty_name} (avoid ','):", bg="#1e1e1e", fg="white").place(x=10, y=5)
    new_prettyname_input = Text(rename_mc_popup_tk, height=1, width=30, fg="white", bg="#464646")
    new_prettyname_input.place(x=10, y=40)

    Button(rename_mc_popup_tk, text="Rename", fg="white", bg="#464646", command=lambda f=filename: rename_connection(f)).place(x=300, y=35)

def kill_popups():
    global ac_popup_tk, mc_popup_tk, rename_mc_popup_tk

    # This functions kills all popup window already opened when you open a new popup window

    try:
        ac_popup_tk.destroy()
    except NameError:
        pass

    try:
        mc_popup_tk.destroy()
    except NameError:
        pass

    try:
        rename_mc_popup_tk.destroy()
    except NameError:
        pass

# Main program

print("Elevating with sudo...")
subprocess.run(["sudo", "echo", "Done!"])

# Setting up the window
root_tk = Tk() # base Tk, named root_tk
root_tk.geometry(f"{800}x{870}") # window size
root_tk.title("Wireguard Connections Manager")
root_tk.configure(bg="#1e1e1e")

main_title = Label(root_tk, text="Wireguard Connection Manager", font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e")
main_title.place(x=10, y=8)

ttk.Separator(root_tk, orient="horizontal").pack(fill="x", pady=40)

Label(root_tk, text="Configure connections :", fg="white", bg="#1e1e1e").place(x=10, y=55)

# "add a connection" part
add_button = Button(root_tk, text="Add a Wireguard Connection", command=add_connection, fg="white", bg="#464646")
add_button.place(x=285, y=50)

# manage connections button
manage_button = Button(root_tk, text="Manage Wireguard Connections", command=manage_connections, fg="white", bg="#464646")
manage_button.place(x=530, y=50)

ttk.Separator(root_tk, orient="horizontal").pack(fill="x", pady=15)

# Available connections display
Label(root_tk, text="Available connections :", fg="white", bg="#1e1e1e").place(x=10, y=105)

available_connections_cnv = Canvas(
    root_tk,
    width=780,
    height=670,
    bg="#1B1B1B"
)
available_connections_cnv.place(x=10, y=145)

refresh_btn = Button(root_tk, text="Refresh List", command=display_all_connections_available, fg="white", bg="#464646")
refresh_btn.place(x=670, y=103)

display_all_connections_available()

# subprocess.run(["sudo","ls","/etc/wireguard"]) 

# Textbox, can be used for the pretty name of the connection
# textbox = Text(root_tk, height=10, width=40)
# textbox.pack()

Button(root_tk, text="Quit", command=quit, fg="white", bg="#464646").place(x=730, y=830)

# icon management
icon = PhotoImage(file=f"{MANAGER_INSTALL_PATH}/pywg-icon.png")
root_tk.iconphoto(True, icon)

root_tk.mainloop()