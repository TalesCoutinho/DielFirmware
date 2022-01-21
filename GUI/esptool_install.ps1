Write-Output "ESP Install"

Invoke-WebRequest -O esptool.zip https://github.com/espressif/esptool/archive/refs/heads/master.zip

Expand-Archive .\esptool.zip

Set-Location .\esptool\

Set-Location .\esptool-master\

python .\setup.py install

Write-Output "ESP Install - Completo"