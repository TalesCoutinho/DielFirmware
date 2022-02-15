$ErrorActionPreference = 'stop'
$source = 'https://www.python.org/ftp/python/3.9.8/python-3.9.8-amd64.exe'
$destination = 'python.exe'
try{ 

    if(Test-Path $env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe){
        Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe
    }
    if(Test-Path $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.exe){
        Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.exe
    }
    if(Test-Path $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.7.exe){
        Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.7.exe
    }

    Invoke-WebRequest -Uri $source -OutFile $destination

    .\python.exe

}
catch{
    Write-Output "Erro"
}