$ErrorActionPreference = 'stop'
Write-Output "ESP Install"
try{

Invoke-WebRequest -O esptool.zip https://github.com/espressif/esptool/archive/refs/heads/master.zip

Expand-Archive .\esptool.zip

Set-Location .\esptool\

Set-Location .\esptool-master\

try{
py -3 .\setup.py install
}
catch{
    try{
        python3 .\setup.py install
    }
    catch{
        try{
            python .\setup.py install
        }
        catch{
            Write-Output "Erro"
        }
    }
}


Copy-Item "..\..\bootloader.bin" -Destination .\
Copy-Item "..\..\ota_data_initial.bin" -Destination .\
Copy-Item "..\..\partitions.bin" -Destination .\ 

Write-Output "ESP Install - Completo"
}
catch{
Write-Output "Erro"
}