$ErrorActionPreference = 'stop'

Write-Output "ESP Command"

$port = $args[0]

$bin = $args[1]

try{
Set-Location .\esptool\

Set-Location .\esptool-master\
try{
    python3 esptool.py --chip esp32 --port $port --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 $bin 0x8000 partitions.bin
    Write-Output "python3"
    }
catch{
    try{
        python esptool.py --chip esp32 --port $port --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 $bin 0x8000 partitions.bin
        Write-Output "python"
    }
    catch{
        try{
            py -3 esptool.py --chip esp32 --port $port --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 $bin 0x8000 partitions.bin
            Write-Output "py -3"
        }
        catch{
            Write-Output "Erro"
        }
    }
}
Set-Location ..

Set-Location ..


Write-Output "ESP Commands - Completo"
}
catch{
Write-Output "Erro"
}