#!/usr/bin/python

def raise_frame(frame):
    frame.tkraise()

def destroy_widgets(frame):
    # clear widgets in next frame
    for widget in frame.winfo_children():
        widget.destroy()

def first_window(f1):
    global map_img
    map = "drone_map_sat.png"
    map_img = ImageTk.PhotoImage(Image.open(map))
    Label(f1, image = map_img).pack(side = "bottom", fill = "both", expand = "yes")
    raise_frame(f1)
    destroy_widgets(f2)
    f1.after(5000,scanDrones, f2)

def scanDrones(f2):
    raise_frame(f2)
    #"1A:D6:C7" is for TESTING ONLY
    mac_address ={"DJI": ["60:60:1F", "1A:D6:C7"], "Parrot": ["A0:14:3D", "90:3A:E6", "90:03:B7", "00:26:7E", "00:12:1C"], "Lily": ["3C:67:16"], "GoPro": ["F4:DD:9E", "D8:96:85", "D4:D9:19", "04:41:69"]}

    # check for cross platform functionality
    if platform == "linux" or platform == "linux2":
        scan_cmd_linux(mac_address)
    elif platform == "darwin":
        # command to get APs for OS X - not available yet
        pass
    elif platform == "win32":
        scan_cmd_windows(mac_address)
    return

def scan_cmd_windows(mac_address):
    os.popen("netsh wlan disconnect")
    time.sleep(1)

    for key in mac_address:
        for item in mac_address[key]:
            print(item)
            scan = os.popen('netsh wlan show network mode=bssid | findstr \"'+item.lower()+' Signal\"').read()
            if 'BSSID' in scan:
                print("scanning for "+item)
                pos = scan.find('BSSID')
                quality = scan[pos:].split('Signal')
                quality = quality[1].split(':')
                quality = quality[1].split('%')
                dBm = (int(quality[0]) / 2) - 100
                show_alert(key,dBm)
                return

def scan_cmd_linux(mac_address):
    for key in mac_address:
        for item in mac_address[key]:
            print(item)
            # scan = os.popen("sudo iwlist wlan0 scan")
            # scan = os.popen("airodump-ng -d "+item.lower()+":00:00:00 -m FF:FF:FF:00:00:00 wlan0").read()
            # more commands to filter results from scan
    return

def show_alert(drone,dBm):
    global drone_img
    distance = get_distance(dBm)
    distance=round(distance,2)

    text_file = open("logs.txt", "a")
    text_file.write("\n "+str(datetime.datetime.now())+" Drone detected in approximately "+str(distance)+"meters.")
    text_file.close()

    Label(f2, text='\n\n ALERT \n ', fg="red",font = "Verdana 10 bold").pack()
    Label(f2, text='\n DRONE '+drone+' detected in approximately '+str(distance)+' meters \n\n{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()),font = "Verdana 10 bold").pack()
    drone_img = ImageTk.PhotoImage(Image.open(drone+".png"))
    Label(f2, image = drone_img).pack(side = "bottom", fill = "both", expand = "yes")
    play_sound()
    f2.after(7000, no_drone,f3)
    return

def no_drone(f3):
    destroy_widgets(f1)
    first_window(f1)

def play_sound():
    return PlaySound("alert.wav", SND_FILENAME)

def get_distance(signal):
    #calculate distance (m)
    frequency = 2412 #frequency (MHz)
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

if __name__ == "__main__":
    from tkinter import *
    from winsound import *
    from PIL import Image,ImageTk
    import math
    from sys import platform
    import os
    import datetime
    import time

    root = Tk()
    root.title("ENISA - Drone Detector")
    f1 = Frame(root)
    f2 = Frame(root)
    f3 = Frame(root)
    f4 = Frame(root)

    for frame in (f1, f2, f3, f4):
        frame.grid(row=0, column=0, sticky='news')

    first_window(f1)

    root.mainloop()
