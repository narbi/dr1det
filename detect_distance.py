#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import math
import os

top = Tk()
top.geometry("200x200")

def scanDrones():
    mac_addresses = ["60:60:1F", "90:03:B7", "A0:14:3D", "00:12:1C", "00:26:7E"]

    # add check for OS
    scan = os.popen("netsh wlan show network mode=bssid").read()

    #get frequency
    frequency = 2412  #MHz

    #get signal level
    signalLevel = -57 #dbm

    distance = math.pow(10,((27.55 - (20 * math.log10(frequency)) + signalLevel)/20))

    messagebox.showinfo( "Searching..", distance)

screen = Button(top, text ="start scanning", command = scanDrones)

screen.place(x=100, y=100)
top.mainloop()