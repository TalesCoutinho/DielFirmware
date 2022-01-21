$ErrorActionPreference = 'stop'

Write-Output "Load Files"

$FileName = $args[0]

$URL = $args[1]

try{
Set-Location .\esptool\

Set-Location .\esptool-master\

if (Test-Path -Path $FileName) {
      Remove-Item $FileName
}


# Copy-Item "..\..\..\..\$FileName" -Destination ".\esptool\esptool-master"

Invoke-WebRequest -O $FileName $URL
# try{
# Expand-Archive .\$FileName
# Write-Output 'A'
# }
# catch{
# $7zipPath = "$env:ProgramFiles\7-Zip\7z.exe"

# if (-not (Test-Path -Path $7zipPath -PathType Leaf)) {
#     throw "7 zip file '$7zipPath' not found"
# }

# Set-Alias 7zip $7zipPath

# 7zip e $FileName
# Write-Output 'A'
# }

Write-Output "Load Files - Completo"
}
catch{
    Write-Output "Erro"
}