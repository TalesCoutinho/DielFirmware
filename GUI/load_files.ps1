$ErrorActionPreference = 'stop'

Write-Output "Load Files"

$FileName = $args[0]

try{


    
    Set-Location .\esptool\

    Set-Location .\esptool-master\

    if (Test-Path -Path $FileName) {
        Remove-Item $FileName
    }

    Copy-Item "..\..\$FileName" -Destination ".\"

    Set-Location ..
    Set-Location ..
    
    if (Test-Path -Path $FileName) {
        Remove-Item $FileName
    }
Write-Output "Load Files - Completo" 
}
catch{
    Write-Output "Erro"
}