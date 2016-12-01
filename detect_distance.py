#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import math
from sys import platform
import os

def scanDrones():
    mac_addresses = ["60:60:1F", "90:03:B7", "A0:14:3D", "00:12:1C", "00:26:7E"]

    # check for cross platform functionality
    if platform == "linux" or platform == "linux2":
        scan = os.popen("airodump-ng -d "+mac_addresses[0]+":00:00:00 -m FF:FF:FF:00:00:00 wlan0").read()
    elif platform == "darwin":
        # command to get APs for OS X
        scan = ""
    elif platform == "win32":
        scan = os.popen("netsh wlan show network mode=bssid | finstr "+mac_addresses[0]+" Signal").read()

    ########
    #dummy set of frequency (MHz)
    frequency = 2412
    #dummy set of signal level (dbm)
    signalLevel = -57
    ########
    distance = get_distance(frequency, signalLevel)
    messagebox.showinfo( "Drone detected", distance )

def get_distance(freq, signal):
    #calculate distance (m)
    distance = math.pow(10,((27.55 - (20 * math.log10(freq)) + signal)/20))
    return distance


top = Tk()
top.geometry("200x200")

screen = Button(top, text ="Start scanning", command = scanDrones)
screen.place(x=100, y=100)

top.mainloop()