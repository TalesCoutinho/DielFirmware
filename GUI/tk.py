from distutils import command
from fileinput import filename
import tkinter as tk
from turtle import width
from typing import Collection, final
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import sys,os, time
import platform
from random import randint
import serial,serial.tools.list_ports
import subprocess

import requests
import json

import logging

import ctypes, enum


    # c = subprocess.run(["powershell", "./cleanup.ps1"],stdout=sys.stdout)
    # for line in iter(c.stdout.readline,''):
    #     if line.rstrip() == 'Erro':
    #         logging.error('Erro ao limpar o sistema')
    #         ttk.dialogs.Messagebox.ok(message = 'Erro', alert=False, parent=None)
    #         flag = False

usb_port_list = []
baud = ""
cb1 = ''
cbc0 = ''
token = ''
user = ''
password = ''

logging.basicConfig(filename='log_file.log', level=logging.WARNING,
                    format='%(asctime)s:%(levelname)s:%(message)s')





def upgrade_python():
    p = subprocess.run(["powershell", "./python_install.ps1"],stdout=sys.stdout)
    for line in iter(p.stdout.readline,''):
        if line.rstrip() == 'Erro':
            logging.error('Erro ao instalar o python')
            ttk.dialogs.Messagebox.ok(message = 'Erro ao atualizar o sistema', alert=False, parent=None)


def upgrade_esptool():
    p = subprocess.run(["powershell", "./esptool_install.ps1"],stdout=sys.stdout)
    for line in iter(p.stdout.readline,''):
        if line.rstrip() == 'Erro':
            logging.error('Erro ao instalar o esptool')
            ttk.dialogs.Messagebox.ok(message = 'Erro ao atualizar o sistema', alert=False, parent=None)

def popup_system():
    python_version = os.popen('python --version').readlines()
    esptool_version = os.popen('esptool.py version').readlines()
    esptool_has_file = os.popen('Microsoft.PowerShell.Management\Test-Path .\esptool').readlines()
    print(esptool_has_file)

    if(python_version[0] != "Python 3.9.8\n"):
        if(ttk.dialogs.Messagebox.show_question(message = 'Python desatualizado, gostaria de atualizar?', parent=None) == 'Yes'):
            upgrade_python()
    if(esptool_has_file != "True" or esptool_version[0] != "esptool.py v3.2\n"):
        if(ttk.dialogs.Messagebox.show_question(message = 'Esptool desatualizado, gostaria de atualizar?', parent=None) == 'Yes'):
            upgrade_esptool()
    else:
        ttk.dialogs.Messagebox.ok(message = 'Sistema atualizado', title='Sistema atualizado', alert=False, parent=None)

# 






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
                

def firmware(FileName, bin):
    URL = FileName + bin
    flag = True

    global cbc0
    print(cbc0.get())

    global cb1
    port = cb1.get()[0] + cb1.get()[1] + cb1.get()[2] + cb1.get()[3]
    print(port)
    

    a = subprocess.run(["powershell", "./load_files.ps1 "+ FileName + " " + URL],stdout=sys.stdout)
    for line in iter(a.stdout.readline,''):
        if line.rstrip() == 'Erro':
            logging.error('Erro ao baixar os arquivos do bash')
            ttk.dialogs.Messagebox.ok(message = 'Erro', alert=False, parent=None)
            flag = False


    b = subprocess.run(["powershell", "./esp_command.ps1 "+ port + " " + bin],stdout=sys.stdout)
    for line in iter(b.stdout.readline,''):
        if line.rstrip() == 'Erro':
            logging.error('Erro de comunicação com a porta serial')
            ttk.dialogs.Messagebox.ok(message = 'Erro', alert=False, parent=None)
            flag = False



    if (flag == True):
        ttk.dialogs.Messagebox.ok(message = 'Firmware atualizado', title='Firmware atualizado', alert=False, parent=None)



class main_window:

    def pick_version(self, event):
        global cbc0
        self.cbc1.config(value = self.final_dictionary[cbc0.get()])
        self.cbc1.current(0)


    def __init__(self, root):
        subprocess.run(["powershell", "-Command", 'Set-ExecutionPolicy RemoteSigned'])

        self.final_dictionary = {}

        global token
        url = 'https://api.dielenergia.com/devs/get-firmware-versions-v2'
        body = {"fwTypes":["prod"]}
        headers = {'Content-Type':'application/json;charset=utf-8','Authorization':'Bearer '+token}
        response = requests.post(url, data = json.dumps(body), headers=headers)
        response = response.content.decode("utf-8")
        response = json.loads(response)
        response = response["list"]


        for element in response:
            if element['hwRev'] in self.final_dictionary:
                self.final_dictionary[element['hwRev']].append(element['fwVers'])
            else:
                self.final_dictionary[element['hwRev']] = [element['fwVers']]




        # Left Frame
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(column= 0, row = 0,padx= 10, pady= 10)

        self.b1 = ttk.Button(self.left_frame, text="Verificar sistema", bootstyle=(INFO, OUTLINE),command = popup_system)
        self.b1.grid(column= 0, row = 0, padx=5, pady=2)


        # Central frame
        self.central_frame = tk.Frame(root)
        self.central_frame.grid(column = 1,row=0, padx = 10, pady=10)

        global cbc0
        self.cbc0Label = ttk.Label(self.central_frame, text='Selecionar placa')
        self.cbc0Label.grid(row = 0, column = 0,pady= 2)
        cbc0 = ttk.Combobox(self.central_frame, values = list(self.final_dictionary.keys()))
        cbc0.bind('<<ComboboxSelected>>', self.pick_version)
        # cbc0.current(0)
        cbc0.grid(column = 0, row = 1,pady= 3)

        self.cbc1Label = ttk.Label(self.central_frame, text='Selecionar versão')
        self.cbc1Label.grid(column = 0, row = 2,pady= 2)
        self.cbc1 = ttk.Combobox(self.central_frame, values = [" "])
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
        self.b4 = ttk.Button(self.right_frame, text="Atualizar o firmware", bootstyle=(INFO, OUTLINE),command = self.get_params)
        self.b4.grid(row = 3, padx=5, pady=5)

    def get_params(self):
        FileName = cbc0.get() + "/" + self.cbc1.get()
        bin = self.cbc1.get() + ".bin"
        firmware(FileName, bin)







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
        if(response == "Invalid password"):
            ttk.dialogs.Messagebox.ok(message = 'Usuário ou senha incorretos', title='Login fail', alert=False, parent=None)
        else:
            response=json.loads(response)
            token = response["token"]
            self.openMainWindow()
        
    def openMainWindow(self):
        root = self.root
        self.newWindow = tk.Toplevel(root)
        self.app = main_window(self.newWindow)





    

if __name__ == '__main__':
    root = ttk.Window(themename="darkly")
    app = tela_login(root)
    root.mainloop()
