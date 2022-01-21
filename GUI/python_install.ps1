$ErrorActionPreference = 'stop'
$source = 'https://www.python.org/ftp/python/3.9.8/python-3.9.8-amd64.exe'
$destination = 'python.exe'
try{
Invoke-WebRequest -Uri $source -OutFile $destination

.\python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

Write-Output "Python instalado"
}
catch{
Write-Output "Erro"
}