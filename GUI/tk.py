import tkinter as tk
from typing import Collection
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import sys,os, time
import platform
from random import randint
import serial,serial.tools.list_ports
import subprocess

import ctypes, enum


usb_port_list = []
baud = ""
cb2 = ''


def upgrade_system():
    p = subprocess.run(["powershell", "./upgrade_system.ps1"],stdout=sys.stdout)
    p.communicate()

def popup():
    python_version = os.popen('python --version').readlines()
    if(python_version[0] == "Python 3.9.7\n"):
        ttk.dialogs.Messagebox.ok(message = 'Sistema atualizado', title='Sistema atualizado', alert=False, parent=None)
    else:
        if(ttk.dialogs.Messagebox.show_question(message = 'Sistema desatualizado, gostaria de atualizar?', parent=None) == 'Yes'):
            upgrade_system()




def find_USB_device(USB_DEV_NAME=None):
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print(myports)
    global usb_port_list
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
                print(usb_id[0])
                return usb_id
                
class GroupClass():
    def connect(self):
        global cb2
        baud = cb2.get()
        self.desc.setText("")
        self.desc.setText(">> trying to connect to port %s ..." % self.typeBox.currentText())
        if self.serial is None:
            self.serial=serial.Serial(self.typeBox.currentText(), baud, timeout=1)
            time.sleep(0.05)
            #self.serial.write(b'hello')
            answer=self.readData()
            if answer!="":
                self.desc.setText(self.desc.toPlainText()+"\n>> Connected!\n"+answer)
        else:
            self.desc.setText(">> {} already Opened!\n".format(self.typeBox.currentText()))

    def sendData(self):
        if self.serial.isOpen():
            if self.title.text() != "":
                self.serial.write(self.title.text().encode())
                answer=self.readData()
                if(self.title.text().encode()=="scan"):
                    print("scanning results -> "+answer.find("0x"))
                else:
                    print(answer.find("0x"))
                self.desc.setText(self.desc.toPlainText()+"\n"+answer)

    def readData(self):
        self.serial.flush() # it is buffering. required to get the data out *now*
        answer=""
        while  self.serial.inWaiting()>0: #self.serial.readable() and
                answer += "\n"+str(self.serial.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
        return answer   

def firmware():

    p = subprocess.run(["powershell", "./load_files.ps1"],stdout=sys.stdout)
    p.communicate()

    port = usb_port_list[0]
    bin = '1_7_7.bin'

    os.system('python ..\esptool\esptool-master\esptool.py --chip esp32 --port '+ port +' --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 '+ bin +' 0x8000 partitions.bin')
  

def check_cbox():
    global baud
    global cb2
    print(cb2.get())
    if cb2.get() != baud:
        baud = cb2.get()


def main():
    subprocess.run(["powershell", "-Command", 'Set-ExecutionPolicy RemoteSigned'])
    root = ttk.Window(themename="darkly")

    # Left Frame
    left_frame = tk.Frame(root)
    left_frame.grid(column= 0, row = 0,padx= 10, pady= 10)

    b1 = ttk.Button(left_frame, text="Verificar sistema", bootstyle=(INFO, OUTLINE),command = popup)
    b1.grid(column= 0, row = 0, padx=5, pady=10)

    b2 = ttk.Button(left_frame, text="Atualizar o firmware", bootstyle=(INFO, OUTLINE),command = firmware)
    b2.grid(column= 0, row = 1, padx=5, pady=10)


    # Central frame
    central_frame = tk.Frame(root)
    central_frame.grid(column = 1,row=0, padx = 10, pady=10)

    cbc0 = ttk.Combobox(central_frame, values = ['DAC', 'DUT', 'DAM', 'DRI'])
    cbc0.current(0)
    cbc0.grid(column = 0, row = 0,pady= 5)

    cbc1 = ttk.Combobox(central_frame, values = ['1', '2', '3', '4'])
    cbc1.current(0)
    cbc1.grid(column = 0, row = 1,pady= 5)

    # Right frame

    right_frame = tk.Frame(root)
    right_frame.grid(column = 3,row=0, padx = 5, pady=5)

    content = GroupClass()

    cb1 = ttk.Combobox(right_frame, values = find_USB_device())
    cb1.grid(column = 0, row = 0, pady = 5)

    global cb2
    cb2 = ttk.Combobox(right_frame, values = ['1200', '2400', '4800', '9600', '115200'])
    cb2.current(0)
    cb2.grid(column = 1, row = 0, pady = 5)

    connect_bt = ttk.Button(right_frame, text="Conectar", bootstyle=(INFO, OUTLINE), command = content.connect)
    connect_bt.grid(column = 2, row = 0)


    place_holder = tk.Text(right_frame, width = 60, height= 10)
    place_holder.grid( column= 0, row = 1, columnspan = 3)

    root.mainloop()


if __name__ == '__main__':
    main()