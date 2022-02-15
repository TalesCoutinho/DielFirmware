import subprocess
import requests
from subprocess import Popen, PIPE


if __name__ == '__main__':
    flag = True
    port = "COM5"
    bin = '1_8_4.bin'
    p = subprocess.Popen(["powershell","./esp_command.ps1 "+ port + " " + bin], stdout=subprocess.PIPE)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            if("Failed to connect to ESP32" in line):
                 print("Impossível conectar com a placa")
                 print("Verifique a porta COM e o log")
                 flag = False
                 break
            if("a" in line):
                print("Deu merda")
                flag = False
                break
        if(flag == True):
            print("Firmware passado com sucesso")
        

            

