$ErrorActionPreference = 'stop'
try{
    $arg = python --version
    Write-Output $arg
}
catch{
    try{
        $arg = python3 --version
        Write-Output $arg
    }
    catch{
        try{
            $arg = py -3 --version
            Write-Output $arg
        }
        catch{
            Write-Output "Erro"
        }
    }
}