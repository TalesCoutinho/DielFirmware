from fileinput import filename
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import sys,os
import serial
import subprocess

import requests
import json #native

import logging




usb_port_list = []
baud = ""
cb1 = ''
cbc0 = ''
token = ''
user = ''
password = ''

logging.basicConfig(filename='log_file.log', level=logging.WARNING,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_log():
    subprocess.run(["powershell", "./log_file.log"])

def yes_no_popup_error(error_message):
    a = tk.Toplevel(root)
    a.title('Mensagem de erro')
    photo = tk.PhotoImage(file = "Logo.png")
    a.iconphoto(False, photo)


    label = ttk.Label(a,text=error_message + "Gostaria de ver o Log?")
    label.grid(column= 0, row = 0, padx = 30, pady = 20)

    button0 = ttk.Button(a, text="Sim", bootstyle=(INFO, OUTLINE),command = get_log)
    button0.grid(column= 0, row = 1, padx = 15, pady = 5)
                
    button1 = ttk.Button(a, text="Fechar", bootstyle=(INFO, OUTLINE),command = a.destroy)
    button1.grid(column= 1, row = 1, padx = 15, pady = 5)



#, command = change_to_yes(return_value, a)
def ok_popup_message(message):
    global return_value
    return_value = 'No'
    a = tk.Toplevel(root)
    a.title('Diel Energia')
    photo = tk.PhotoImage(file = "Logo.png")
    a.iconphoto(False, photo)


    label = ttk.Label(a,text=message)
    label.grid(column= 0, row = 0, padx = 30, pady = 10)

    button0 = ttk.Button(a, text="Ok", bootstyle=(INFO, OUTLINE), command = a.destroy)
    button0.grid(column= 0, row = 1, padx = 5, pady = 5)

    return return_value

def run_ps_file(file_name, error_message, log_message, success_name):
    p = subprocess.Popen(["powershell",file_name], stdout=subprocess.PIPE)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            if(line == 'Erro\r\n'):
                logging.error(log_message)
                yes_no_popup_error(error_message)
                return
    ok_popup_message(success_name + ' finalizado com sucesso.')
    
                




def on_closing():
    root.destroy()

def upgrade_python():
    run_ps_file('./python_install.ps1', 'Erro ao instalar o python. ','Erro ao instalar o python','Python instalado com sucesso')
            


def upgrade_esptool():
    run_ps_file('./esptool_install.ps1', 'Erro ao instalar o esptool.  ','Erro ao instalar o esptool', 'Esptool instalado com sucesso')

def popup_system():
    python_version = os.popen('python --version').readlines()
    esptool_version = os.popen('esptool.py version').readlines()
    esptool_has_file = os.path.exists('./esptool')

    if(python_version[0] != "Python 3.9.8\n" or esptool_has_file != True or esptool_version[0] != "esptool.py v3.2\n"):
        ok_popup_message('Sistema desatualizado, realizando atualizações')
        if(python_version[0] != "Python 3.9.8\n"):
            upgrade_python()
        if(esptool_has_file != True or esptool_version[0] != "esptool.py v3.2\n"):
            upgrade_esptool()
    else:
        ok_popup_message('Sistema atualizado.')







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
    flag = True

    global cbc0

    global cb1
    port = cb1.get()[0] + cb1.get()[1] + cb1.get()[2] + cb1.get()[3]

    url = 'https://api.dielenergia.com/get-firmware-file/prod/'+FileName+'.bin'
    headers = {'Authorization':'Bearer '+token}
    r = requests.get(url, headers, allow_redirects=True)
    open(bin, 'wb').write(r.content)
    

    run_ps_file("./load_files.ps1 "+ bin, 'Erro ao baixar os arquivos.  ', 'Erro ao passar os arquivos binários para a pasta do esptool. ', 'Arquivos organizados com sucesso')

    run_ps_file("./esp_command.ps1 "+ port + " " + bin, 'Erro ao passar o firmware. Verifique a porta COM. ', 'Erro ao rodar o comando do esptool', 'Firmware passado com sucesso')

    if (flag == True):
        ok_popup_message('Firmware atualizado')


class gravacao_firmware:

    def pick_version(self, event):
        global cbc0
        self.cbc1.config(value = self.final_dictionary[cbc0.get()])
        self.cbc1.current(0)


    def __init__(self, root):
        # root.protocol("WM_DELETE_WINDOW", on_closing)
        subprocess.run(["powershell", "-Command", 'Set-ExecutionPolicy RemoteSigned'], capture_output=True, text=True, input="A")
        photo = tk.PhotoImage(file = "Logo.png")
        root.iconphoto(False, photo)

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
        self.app = menu(self.newWindow)
        self.root.withdraw()

class menu:
    def __init__(self, root):
        root.protocol("WM_DELETE_WINDOW", on_closing)
        photo = tk.PhotoImage(file = "Logo.png")
        root.title('Diel Energia')
        root.iconphoto(False, photo)
        self.frame = tk.Frame(root)
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
        root.withdraw()







    

if __name__ == '__main__':
    root = ttk.Window("Diel Energia",themename="darkly")
    photo = tk.PhotoImage(file = "Logo.png")
    root.iconphoto(False, photo)
    app = tela_login(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

