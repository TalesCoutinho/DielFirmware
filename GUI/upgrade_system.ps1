# $source = 'https://www.python.org/ftp/python/3.9.8/python-3.9.8-amd64.exe'
# $destination = 'C:\Users\Tales\Documents\New Folder\python.exe'
# Invoke-WebRequest -Uri $source -OutFile $destination

# .\python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

Set-Location ..

Invoke-WebRequest -O esptool.zip https://github.com/espressif/esptool/archive/refs/heads/master.zip

Expand-Archive .\esptool.zip

Set-Location .\esptool\

Set-Location .\esptool-master\

python .\setup.py install