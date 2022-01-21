from distutils import command
import tkinter as tk
from turtle import width
from typing import Collection
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import sys,os, time
import platform
from random import randint
import serial,serial.tools.list_ports
import subprocess

import requests
import json

import ctypes, enum


usb_port_list = []
baud = ""
cb1 = ''
cbc0 = ''
token = ''
user = ''
password = ''





def upgrade_python():
    p = subprocess.run(["powershell", "./python_install.ps1"],stdout=sys.stdout)
    p.communicate()

def upgrade_esptool():
    p = subprocess.run(["powershell", "./esptool_install.ps1"],stdout=sys.stdout)
    p.communicate()

def popup_system():
    python_version = os.popen('python --version').readlines()
    esptool_version = os.popen('esptool.py version').readlines()

    if(python_version[0] == "Python 3.9.8\n"):
        ttk.dialogs.Messagebox.ok(message = 'Python atualizado', title='Python atualizado', alert=False, parent=None)
    else:
        if(ttk.dialogs.Messagebox.show_question(message = 'Python desatualizado, gostaria de atualizar?', parent=None) == 'Yes'):
            upgrade_python()

    if(esptool_version[0] == "esptool.py v3.2\n"):
        ttk.dialogs.Messagebox.ok(message = 'Esptool atualizado', title='Esptool atualizado', alert=False, parent=None)
    else:
        if(ttk.dialogs.Messagebox.show_question(message = 'Esptool desatualizado, gostaria de atualizar?', parent=None) == 'Yes'):
            upgrade_python()







def find_USB_device(USB_DEV_NAME=None):
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
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
                

def firmware():
    FileName = ''
    URL = ''
    bin = ''

    global cbc0
    print(cbc0.get())

    global cb1
    port = cb1.get()[0] + cb1.get()[1] + cb1.get()[2] + cb1.get()[3]
    print(port)
    
    if(cbc0.get() == 'DAC'):
        FileName = '.\dac4_1_5_2.rar'
        URL = X
        bin = '1_5_2.bin'
    if(cbc0.get() == 'DUT'):
        FileName = '.\dut3_1_7_7.7z'
        URL = X
        bin = '1_7_7.bin'
    if(cbc0.get() == 'DRI'):
        return

    subprocess.run(["powershell", "./load_files.ps1 "+ FileName + " " + URL],stdout=sys.stdout)


    subprocess.run(["powershell", "./esp_command.ps1 "+ port + " " + bin],stdout=sys.stdout)


    subprocess.run(["powershell", "./cleanup.ps1"],stdout=sys.stdout)

    ttk.dialogs.Messagebox.ok(message = 'Firmware atualizado', title='Firmware atualizado', alert=False, parent=None)



class main_window:
    def __init__(self, root):
        subprocess.run(["powershell", "-Command", 'Set-ExecutionPolicy RemoteSigned'])

        # Left Frame
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(column= 0, row = 0,padx= 10, pady= 10)

        self.b1 = ttk.Button(self.left_frame, text="Verificar sistema", bootstyle=(INFO, OUTLINE),command = popup_system)
        self.b1.grid(column= 0, row = 0, padx=5, pady=2)


        # Central frame
        self.central_frame = tk.Frame(root)
        self.central_frame.grid(column = 1,row=0, padx = 10, pady=10)

        global cbc0
        self.usernameLabel = ttk.Label(self.central_frame, text='Selecionar placa')
        self.usernameLabel.grid(row = 0, column = 0,pady= 2)
        cbc0 = ttk.Combobox(self.central_frame, values = ['DAC', 'DUT', 'DAM', 'DRI'])
        cbc0.current(0)
        cbc0.grid(column = 0, row = 1,pady= 3)

        self.usernameLabel = ttk.Label(self.central_frame, text='Selecionar versão')
        self.usernameLabel.grid(column = 0, row = 2,pady= 2)
        self.cbc1 = ttk.Combobox(self.central_frame, values = ['1', '2', '3', '4'])
        self.cbc1.current(0)
        self.cbc1.grid(column = 0, row = 3,pady= 5)

        # Right frame

        self.right_frame = tk.Frame(root)
        self.right_frame.grid(column = 3,row=0, padx = 5, pady=5)

        self.usernameLabel = ttk.Label(self.right_frame, text='Selecionar porta')
        self.usernameLabel.grid(column = 0, row = 0,pady= 2)
        global cb1
        cb1 = ttk.Combobox(self.right_frame, values = find_USB_device())
        cb1.current(len(find_USB_device())-1)
        cb1.grid(column = 0, row = 1, pady = 5, padx = 5)


        self.usernameLabel = ttk.Label(self.right_frame, text='')
        self.usernameLabel.grid(column = 0, row = 2,pady= 2)
        self.b4 = ttk.Button(self.right_frame, text="Atualizar o firmware", bootstyle=(INFO, OUTLINE),command = firmware)
        self.b4.grid(row = 3, padx=5, pady=5)







class tela_login:
    def __init__(self, master):
        self.root = master
        self.frame = tk.Frame(self.root)
        self.frame.grid(column= 0, row = 0,padx= 10, pady= 10)

        self.usernameLabel = ttk.Label(self.frame, text='Usuário')
        self.usernameLabel.grid(row = 0, column = 0)
        self.myUsername = tk.StringVar()
        self.username = ttk.Entry(self.frame, width = 40, textvariable=self.myUsername)
        self.username.grid(row = 1, column = 0, pady = 5)

        self.passwordLabel = ttk.Label(self.frame, text='Senha')
        self.passwordLabel.grid(row = 2, column = 0)
        self.myPassword = tk.StringVar()
        self.password = ttk.Entry(self.frame, show="*", width = 40, textvariable= self.myPassword)
        self.password.grid(row = 3, column = 0, pady = 5)

        self.button = ttk.Button(self.frame, text="Conectar", bootstyle=(INFO, OUTLINE), width = 10, command=self.get_credentials)
        self.button.grid(row = 4, column = 0, pady = 5)

    def get_credentials(self):
        global user
        global password
        user = self.myUsername.get()
        password = self.myPassword.get()
        self.login()

    def login(self):
        global user
        global password
        global token
        url = 'https://api.dielenergia.com/login'
        body = {'user':user,'password':password}
        headers = {'Content-Type':'application/json;charset=utf-8'}
        response = requests.post(url, data = json.dumps(body), headers=headers)
        response = response.content.decode("utf-8")
        response=json.loads(response)
        if(response == "b'Invalid password'"):
            ttk.dialogs.Messagebox.ok(message = 'Usuário ou senha incorretos', title='Login fail', alert=False, parent=None)
        else:
            token = response["token"]
        
    def newWindow(self):
        root = self.root
        self.app = main_window(root)





    

if __name__ == '__main__':
    root = ttk.Window(themename="darkly")
    app = tela_login(root)
    root.mainloop()
