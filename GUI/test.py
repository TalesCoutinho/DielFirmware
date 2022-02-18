import subprocess

p = subprocess.run(["powershell", "-Command", 'Set-ExecutionPolicy Bypass'], capture_output=True, text=True, input="A", stdout=subprocess.PIPE)
with p.stdout:
        for line in iter(p.stdout.readline, b''):
            line = line.decode("utf-8")
            print(line)
        