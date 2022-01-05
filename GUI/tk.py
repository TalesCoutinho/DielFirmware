import tkinter as tk
from typing import Collection
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import sys,os, time
import platform
from random import randint
import serial,serial.tools.list_ports

from PIL import Image
from PIL import ImageTk

def popup():
    ttk.dialogs.Messagebox.ok(message = 'Sistema atualizado', title='Sistema atualizado', alert=False, parent=None)

def find_USB_device(USB_DEV_NAME=None):
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print(myports)
    usb_port_list = [p[0] for p in myports]
    usb_device_list = [p[1] for p in myports]
    print(usb_device_list)

    if USB_DEV_NAME is None:
        return myports
    else:
        USB_DEV_NAME=str(USB_DEV_NAME).replace("'","").replace("b","")
        for device in usb_device_list:
            print("{} -> {}".format(USB_DEV_NAME,device))
            print(USB_DEV_NAME in device)
            if USB_DEV_NAME in device:
                print(device)
                usb_id = device[device.index("COM"):device.index("COM")+4]
            
                print("{} port is {}".format(USB_DEV_NAME,usb_id))
                return usb_id
  




root = ttk.Window(themename="darkly")

# Left Frame
left_frame = tk.Frame(root)
left_frame.grid(column= 0, row = 0,padx= 10, pady= 10)

b1 = ttk.Button(left_frame, text="Verificar sistema", bootstyle=(INFO, OUTLINE),command = popup)
b1.grid(column= 0, row = 0, padx=5, pady=10)

b2 = ttk.Button(left_frame, text="Atualizar o firmware", bootstyle=(INFO, OUTLINE))
b2.grid(column= 0, row = 1, padx=5, pady=10)


# Central frame
central_frame = tk.Frame(root)
central_frame.grid(column = 1,row=0, padx = 10, pady=10)

cb0 = ttk.Combobox(central_frame, values = ['DAC', 'DUT', 'DAM', 'DRI'])
cb0.pack(pady= 5)

# Right frame

right_frame = tk.Frame(root)
right_frame.grid(column = 3,row=0, padx = 5, pady=5)

cb1 = ttk.Combobox(right_frame, values = find_USB_device())
cb1.grid(column = 0, row = 0, pady = 5)

cb2 = ttk.Combobox(right_frame, values = ['1200', '2400', '4800', '9600', '115200'])
cb2.grid(column = 1, row = 0, pady = 5)


place_holder = tk.Text(right_frame, width = 60, height= 10)
place_holder.grid( column= 0, row = 1, columnspan = 2)

root.mainloop()