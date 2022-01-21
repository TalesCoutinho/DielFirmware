Write-Output "ESP Command"

$port = $args[0]

$bin = $args[1]

Set-Location .\esptool\

Set-Location .\esptool-master\

python esptool.py --chip esp32 --port $port --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 $bin 0x8000 partitions.bin

Write-Output "ESP Commands - Completo"