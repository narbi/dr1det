#!/usr/bin/python

def raise_frame(frame):
    frame.tkraise()

def destroy_widgets(frame):
    # clear widgets in next frame
    for widget in frame.winfo_children():
        widget.destroy()

def first_window(f1):
    gif = AnimatedGIF(f1, "radar_.gif")
    gif.pack(side = "top", fill = "both", expand = "true", padx = 100, pady = 150)
    raise_frame(f1)
    destroy_widgets(f2)
    f1.after(6250,scanDrones, f2)

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
    # time.sleep(1)
    scan_to_file()
    time.sleep(0.2)
    for key in mac_address:
        for lookup in mac_address[key]:
            print(lookup)

            ssidLine=get_line_number(lookup.lower(),"scans.txt")
            if (ssidLine>0):
                # Search in specific line
                ssid = linecache.getline('scans.txt', ssidLine-4)
                mac = linecache.getline('scans.txt', ssidLine)
                signal=linecache.getline('scans.txt', ssidLine+1)
                channel=linecache.getline('scans.txt', ssidLine+3)
                print(ssid,mac,signal,channel)

                quality = signal.split(':')
                quality = quality[1].split('%')
                dBm = (int(quality[0]) / 2) - 100

                mac = mac.split(':',1)
                ssid = ssid.split(':')
                channel = channel.split(':')
                show_alert(key, dBm, mac[1].strip(), ssid[1].strip(), channel[1].strip())
                return
    first_window(f1)
    return

def scan_cmd_linux(mac_address):
    for key in mac_address:
        for item in mac_address[key]:
            print(item)
            # scan = os.popen("sudo iwlist wlan0 scan")
            # scan = os.popen("airodump-ng -d "+item.lower()+":00:00:00 -m FF:FF:FF:00:00:00 wlan0").read()
            # more commands to filter results from scan
    return

def show_alert(drone,dBm, mac, ssid, channel):
    global drone_img
    distance = get_distance(dBm)
    distance=round(distance,2)

    text_file = open("logs.txt", "a")
    text_file.write("\n"+str(datetime.datetime.now())+"\t"+mac+"\t"+ssid+"\t"+drone+" DRONE\t~"+str(distance)+"m.")
    text_file.close()

    Label(f2, text='\n\n ALERT \n ', fg="red",font = "Verdana 10 bold").pack()
    Label(f2, text='\n DRONE '+drone+' detected in approximately '+str(distance)+' meters \n\n{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()),font = "Verdana 10 bold").pack()
    drone_img = ImageTk.PhotoImage(Image.open(drone+".png"))
    Label(f2, image = drone_img).pack(side = "bottom", fill = "both", expand = "yes")
    play_sound()
    f2.after(7000, first_window,f1)
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

def get_line_number(phrase, file_name):
    f=open(file_name, 'r')
    for (i, line) in enumerate(f,1):
        if phrase in line:
            return i
    return -1


def scan_to_file():
    outfile = open("scans.txt","w")
    subprocess.Popen('netsh wlan show network mode=bssid',stdout=outfile)
    outfile.close()
    return


from tkinter import PhotoImage
from tkinter import Label

from PIL import Image, ImageTk


class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError: pass

        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)

    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)

if __name__ == "__main__":
    from tkinter import *
    from winsound import *
    from PIL import Image,ImageTk
    import math
    from sys import platform
    import os
    import datetime
    import subprocess
    import linecache
    import time


    root = Tk()
    root.title("ENISA - Drone Detector")
    root.minsize(width=500,height=950)
    f1 = Frame(root)
    f2 = Frame(root)
    f3 = Frame(root)
    f4 = Frame(root)

    for frame in (f1, f2, f3, f4):
        frame.grid(row=0, column=0, sticky='news')


    first_window(f1)

    root.mainloop()
