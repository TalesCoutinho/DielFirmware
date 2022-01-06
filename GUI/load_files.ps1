Set-Location .\esptool\

Set-Location .\esptool-master\

$FileName = ".\dut3_1_7_7.7z"

if (Test-Path -Path $FileName) {
      Remove-Item $FileName
    }

Copy-Item "C:\Documentos\dut3_1_7_7.7z" -Destination ".\esptool-master"

#Invoke-WebRequest https://drive.google.com/file/d/1lg4jn7etZiajBolRvQjRMYdKuxSTPhq_/view?usp=sharing

$7zipPath = "$env:ProgramFiles\7-Zip\7z.exe"

if (-not (Test-Path -Path $7zipPath -PathType Leaf)) {
    throw "7 zip file '$7zipPath' not found"
}

Set-Alias 7zip $7zipPath

7zip e $FileName