$bin = "1_8_4.bin"

$COMportList = [System.IO.Ports.SerialPort]::getportnames()
ForEach ($COMport in $COMportList) {
     $temp = new-object System.IO.Ports.SerialPort $COMport
     Write-Output $temp.PortName
     $port = $temp.PortName
     Set-Location ..
     # .\esptool.py --chip esp32 --port $port --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 $bin 0x8000 partitions.bin
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
                  try{
                      .\esptool.py --chip esp32 --port $port --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x19000 ota_data_initial.bin 0x1000 bootloader.bin 0x20000 $bin 0x8000 partitions.bin
                      Write-Output ".\esptool"
                  }
                  catch{
                      Write-Error "Error"
                  }
              }
          }
      }
     $temp.Dispose()
    }