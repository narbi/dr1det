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

def scanDrones(f2):
    raise_frame(f2)
    # 60:60:1F = DJI Phanton
    # 90:03:B7, A0:14:3D, 00:12:1C, 00:26:7E = Parrot
    mac_addresses = ["60:60:1F", "90:03:B7", "A0:14:3D", "00:12:1C", "00:26:7E"]
    # check for cross platform functionality
    # if platform == "linux" or platform == "linux2":
    #     scan = os.popen("airodump-ng -d "+mac_addresses[0]+":00:00:00 -m FF:FF:FF:00:00:00 wlan0").read()
    # elif platform == "darwin":
    #     # command to get APs for OS X
    #     pass
    # elif platform == "win32":

    for i in range (len(mac_addresses)):
        #scan = os.popen("netsh wlan show network mode=bssid | findstr \"00:1d:aa Signal\"").read()
        scan = os.popen("netsh wlan show network mode=bssid | findstr \""+mac_addresses[i]+" Signal\"").read()
        if 'BSSID' in scan:
            pos = scan.find('BSSID')
            quality = scan[pos:].split('Signal')
            quality = quality[1].split(':')
            quality = quality[1].split('%')
            dBm = (int(quality[0]) / 2) - 100
            found = True
            break
        else:
            found = False

    if (found == True):
        distance = get_distance(dBm)
        if distance <= 250 :
            zone = "A"
        else:
            zone = "B"
        # messagebox.showinfo( "Drone detected", "Drone detected in "+str(distance)+" meters")
        Label(f2, text='\n\n\nDrone detected in '+str(distance)+' meters (zone '+zone+') ').pack()
        Button(f2, text='Scan again', command=lambda:raise_frame(f1)).pack()


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

def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title("ENISA - prototype drone radar")
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')


Button(f1, text='Start scanning', command=lambda:scanDrones(f2)).pack()
map_img = ImageTk.PhotoImage(Image.open("drone_map_demo.png"))
panel = Label(f1, image = map_img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
raise_frame(f1)



root.mainloop()
