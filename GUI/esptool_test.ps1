$ErrorActionPreference = 'stop'
try{
    $arg = python ./esptool/esptool-master/esptool.py version
    Write-Output $arg
}
catch{
    try{
        $arg = python3 ./esptool/esptool-master/esptool.py version
        Write-Output $arg
    }
    catch{
        try{
            $arg = py -3 ./esptool/esptool-master/esptool.py version
            Write-Output $arg
        }
        catch{
            Write-Output "Erro"
        }
    }
}