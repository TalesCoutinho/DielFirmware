from asyncio.windows_events import NULL
from fileinput import filename
from msilib.schema import File
import tkinter as tk
from turtle import width
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import sys,os
import serial, serial.tools.list_ports
import subprocess
from subprocess import PIPE, STDOUT, CREATE_NO_WINDOW

import requests
import json #native

import logging

import datetime





usb_port_list = []
baud = ""
cb1 = ''
cbc0 = ''
token = ''
user = ''
password = ''
alert_list = ["","",""]
alert_label0 = ''
alert_label1 = ''
alert_label2 = ''

logging.basicConfig(filename='log_file.log', level=logging.WARNING,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_log():
    subprocess.run(["powershell", "./log_file.log"])




def alert_function(message):
    global alert_list
    now = datetime.datetime.now()
    alert_list.pop()
    alert_list.insert(0, "[{}:{}:{}] - {}".format(now.hour, now.minute, now.second, message))

    global alert_label0
    global alert_label1
    global alert_label2
    alert_label0.config(text = alert_list[2])
    alert_label1.config(text = alert_list[1])
    alert_label2.config(text = alert_list[0])

    
def run_ps_file(file_name, error_message, log_message, success_name):
    flag = True
    alert_function("")
    alert_function("")
    alert_function("Carregando...")
    p = subprocess.Popen(["powershell",file_name], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            if(line == 'Erro\r\n'):
                logging.error(log_message)
                alert_function(error_message)
                flag = False
                return
    if(flag == True):
        alert_function(success_name)
    
def check_drivers():
    has_driver = False
    p = subprocess.Popen(["powershell","Get-ChildItem -Path 'C:\Windows\System32\DriverStore\FileRepository' -Recurse -Directory | Select-String 'ftdibus' -List"], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            if("ftdi" in line):
                has_driver = True

    if(has_driver == False):
        alert_function("Não tem driver FTDI")
        response = requests.get("https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip")
        open('FTDI_DRIVER_SETUP.zip', 'wb').write(response.content)
        install = subprocess.Popen(["powershell", ".\\FTDI_DRIVER_SETUP.zip"], creationflags=CREATE_NO_WINDOW)
        return has_driver
    else:
        alert_function("Tem driver FTDI")
        has_driver = False

    p = subprocess.Popen(["powershell","Get-ChildItem -Path 'C:\Windows\System32\DriverStore\FileRepository' -Recurse -Directory | Select-String 'slabv' -List"], stdout=subprocess.PIPE)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            if("slabv" in line):
                has_driver = True

    if(has_driver == False):
        alert_function("Não tem driver SLABV")
        p = subprocess.Popen(["powershell","Get-ChildItem -Path 'C:\Windows\System32\DriverStore\FileRepository' -Recurse -Directory | Select-String 'slabv' -List"], stdout=subprocess.PIPE)
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                line = line.decode("utf-8")
                if("64" in line):
                    subprocess.Popen(["powershell","./SLABV_X64.exe"], stdout=subprocess.PIPE)
                    return has_driver
                if("32" in line):
                    subprocess.Popen(["powershell","./SLABV_X32.exe"], stdout=subprocess.PIPE)
                    return has_driver
        
    else:
        alert_function("Tem driver SLABV")
        return has_driver




def on_closing():
    root.destroy()

def upgrade_python():
    run_ps_file('./python_install.ps1', 'Erro ao instalar o python. ','Erro ao instalar o python','Python instalado com sucesso')
            


def upgrade_esptool():
    run_ps_file('./esptool_install.ps1', 'Erro ao instalar o esptool.  ','Erro ao instalar o esptool', 'Esptool instalado com sucesso')

def popup_system():
    if(check_drivers() == False):
        alert_function("Verifique o sistema novamente")
        alert_function("após a instalação do driver")
        return False
    python_version = os.popen('py -3 --version').readlines()
    esptool_version = os.popen('py -3 ./esptool/esptool-master/esptool.py version').readlines()
    esptool_has_file = os.path.exists('./esptool')


    if(esptool_version == NULL):
        esptool_version = ''

    if("Python 3." not in python_version[0] or esptool_has_file != True or "esptool.py v3." not in esptool_version[0]):
        alert_function('Sistema desatualizado, realizando atualizações')
        if("Python 3." not in python_version[0]):
            upgrade_python()
            alert_function("Instalando o python")
        if(esptool_has_file != True or "esptool.py v3." not in esptool_version[0]):
            upgrade_esptool()
            alert_function("Instalando o esptool")
    else:
        alert_function('Sistema atualizado.')



def run_esptool(port, bin):
    flag = True
    p = subprocess.Popen(["powershell","./esp_command.ps1 "+ port + " " + bin], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            if("Failed to connect to ESP32" in line):
                 alert_function("Impossível conectar com a placa")
                 alert_function("Verifique a porta COM e o log")
                 logging.error(line)
                 flag = False
                 break
            if("Erro" in line):
                alert_function("Sistema desatualizado")
                logging.error("Esptool não instalado, caminho não encontrado")
                flag = False
                break
        if(flag == True):
            alert_function("Firmware passado com sucesso")
    

def refresh_port_selection():
    global cb1
    ports = find_USB_device()
    cb1.config(value = ports)
    cb1.current(len(find_USB_device())-1)
    for item in ports:
        if("serial" in item):
            cb1.current(ports[ports.index(item)])


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

    global cbc0

    global cb1
    port = cb1.get()[0] + cb1.get()[1] + cb1.get()[2] + cb1.get()[3]

    url = 'https://api.dielenergia.com/get-firmware-file/prod/'+FileName+'.bin'
    headers = {'Authorization':'Bearer '+token}
    r = requests.get(url, headers = headers, allow_redirects=True)
    open(bin, 'wb').write(r.content)

    run_ps_file("./load_files.ps1 "+ bin, 'Erro ao baixar os arquivos.  ', 'Erro ao passar os arquivos binários para a pasta do esptool. ', 'Arquivos organizados com sucesso')

    run_esptool(port,bin)


class gravacao_firmware:

    def pick_version(self, event):
        refresh_port_selection()
        global cbc0
        self.cbc1.config(value = self.final_dictionary[cbc0.get()])
        self.cbc1.current(0)


    def __init__(self, root):
        subprocess.run(["powershell", "-Command", 'Set-ExecutionPolicy RemoteSigned'], capture_output=True, text=True, input="A")
        self.root = root
        photo = tk.PhotoImage(file = "Logo.png")
        self.root.iconphoto(False, photo)

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

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
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(column= 0, row = 0,padx= 10, pady= 10)

        self.b1 = ttk.Button(self.left_frame, text="Verificar sistema", bootstyle=(INFO, OUTLINE),command = popup_system)
        self.b1.grid(column= 0, row = 0, padx=5, pady=2)

        self.b2 = ttk.Button(self.left_frame, text="Abrir log", bootstyle=(INFO, OUTLINE),command = get_log)
        self.b2.grid(column= 0, row = 1, padx=5, pady=2)


        # Central frame
        self.central_frame = tk.Frame(self.root)
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

        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(column = 3,row=0, padx = 5, pady=5)

        self.usernameLabel = ttk.Label(self.right_frame, text='Selecionar porta')
        self.usernameLabel.grid(column = 0, row = 0,pady= 2)
        global cb1
        cb1 = ttk.Combobox(self.right_frame, values = "")
        cb1.grid(column = 0, row = 1, pady = 5, padx = 5)


        self.usernameLabel = ttk.Label(self.right_frame, text='')
        self.usernameLabel.grid(column = 0, row = 2,pady= 2)
        self.b4 = ttk.Button(self.right_frame, text="Atualizar o firmware", bootstyle=(INFO, OUTLINE),command = self.get_params)
        self.b4.grid(row = 3, padx=5, pady=5)

        #Last frame
        self.last_frame = ttk.Labelframe(self.root, text = "Alertas")
        self.last_frame.grid(column = 0,row=1, padx = 10, pady = 10, columnspan= 5)

        global alert_list
        global alert_label0
        global alert_label1
        global alert_label2

        alert_label0 = ttk.Label(self.last_frame, text = alert_list[2])
        alert_label0.grid(column=0, row=0, padx = 160, pady = 10)

        alert_label1 = ttk.Label(self.last_frame, text = alert_list[1])
        alert_label1.grid(column=0, row=1, padx = 160, pady = 10)

        alert_label2 = ttk.Label(self.last_frame, text = alert_list[0])
        alert_label2.grid(column=0, row=2, padx = 160, pady = 10)



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
        self.app = menu(self.newWindow)
        self.root.withdraw()

class menu:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        photo = tk.PhotoImage(file = "Logo.png")
        root.title('Diel Energia')
        root.iconphoto(False, photo)
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=30)
        self.main_label = ttk.Label(self.frame, text= 'Menu')
        self.main_label.grid(column= 0, row=0, pady=5)

        self.firmwareButton = ttk.Button(self.frame, text="Firmware", bootstyle=(INFO, OUTLINE), width = 20, command=self.tela_firmware)
        self.firmwareButton.grid(column= 0, row=1, pady=5, padx=30)

        self.jigaButton = ttk.Button(self.frame, text="JIGA", bootstyle=(INFO, OUTLINE), width = 20)
        self.jigaButton.grid(column= 0, row=2, pady=5, padx=30)

        self.comissionamentoButton = ttk.Button(self.frame, text="Comissionamento", bootstyle=(INFO, OUTLINE), width = 20)
        self.comissionamentoButton.grid(column= 0, row=3, pady=5, padx=30)

    def tela_firmware(self):
        self.newWindow = tk.Toplevel(root)
        self.app = gravacao_firmware(self.newWindow)
        self.root.withdraw()







    

if __name__ == '__main__':
    root = ttk.Window("Diel Energia",themename="darkly")
    photo = tk.PhotoImage(file = "Logo.png")
    root.iconphoto(False, photo)
    app = tela_login(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

