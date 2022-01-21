Write-Output "Cleanup"

Remove-Item .\esptool -Recurse -Force -Confirm:$false

Remove-Item .\esptool.zip -Recurse -Force -Confirm:$false

Write-Output "Cleanup - Completo"
