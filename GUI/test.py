import subprocess

python_version = ''
p = subprocess.Popen(["powershell",".\python_test.ps1"], stdout=subprocess.PIPE)
with p.stdout:
    for line in iter(p.stdout.readline, b''):
        line = line.decode("utf-8")
        if("Python 3." in line):
            python_version = line

print(python_version)
        