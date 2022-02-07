$ErrorActionPreference = 'stop'
$source = 'https://www.python.org/ftp/python/3.9.8/python-3.9.8-amd64.exe'
$destination = 'python.exe'
try{ 
    Write-Output "Rodando a instalação do python"

    if(Test-Path $env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe){
        Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe
    }
    if(Test-Path $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.exe){
        Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.exe
    }

    Invoke-WebRequest -Uri $source -OutFile $destination

    .\python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    Write-Output "Python instalado"


}
catch{
    Write-Output "Erro"
}