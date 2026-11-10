import subprocess
s = subprocess.run(["nmap", "-p-", "127.0.0.1"], capture_output=True, text=True)
if s.returncode == 0:
    with open("portas_abertas.txt", "w") as f:
        for linha in s.stdout.splitlines():
            if "open" in linha:
                print(linha) 
                f.write(linha + "\n") 
else:
    print(f"Ouve um erro... :( \n", s.stderr)
