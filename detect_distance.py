#!/usr/bin/python
from tkinter import *
from tkinter import messagebox

top = Tk()
top.geometry("200x200")
# Code to add widgets will go here...
def helloCallBack():
    messagebox.showinfo( "Hello Python", "Hello World")
    #MAC addresses: 60:60:1F, 90:03:B7, A0:14:3D, 00:12:1C, 00:26:7E
screen = Button(top, text ="Hello", command = helloCallBack)
screen.place(x=100, y=100)
top.mainloop()