from colorama import Fore, init
init(autoreset=True)
import subprocess, os

def ligar():
    s = subprocess.run(["nmcli", "radio", "wifi", "on"], text=True, capture_output=True)
    if s.returncode == 0:
        print("Conexão wi-fi ativa:\n ")
        print(os.system("nmcli radio wifi"))
    else:
        print("Houve um erro de rede: ", s.stderr)

def desligar():
    s = subprocess.run(["nmcli", "radio", "wifi", "off"], text=True, capture_output=True)
    if s.returncode == 0:
        print("Conexão wi-fi: \n")
        print(os.system("nmcli radio wifi"))
    else:
        print("Houve um erro na rede", s.stderr)

def ver_redes():
    print("#" * 45 + "\nREDES:\n")
    print(os.system("nmcli device wifi list"))
    print("#" * 45 + "\nREDES SALVAS:\n")
    print(os.system("nmcli -f name,type,device connection show"))
    print("#" * 45)

def conectar_rede():
    rede = input("Digite o nome da rede wi-fi: ")
    senha = input("Digite a senha: ")
    s = subprocess.run(["nmcli", "device", "wifi", "connect", rede, "password", senha], text=True, capture_output=True)
    if s.returncode == 0:
        print("Conectado em: ")
        print(os.system("nmcli -t -f active,ssid dev wifi"))
    else:
        print("Ocorreu um erro durante a conexão: ", s.stderr)

def ip_estatico():
    print(Fore.RED + "É importante saber que colocando gateway/ip errado você fica sem conexão com a internet!!!")
    print("#" * 50 + "\nO nome da sua rede está em verde!\n")
    print(os.system("nmcli -f name,type,device connection show"))
    rede = input("Digite o nome de sua rede: ")
    print("*" * 35 + "IP: ")
    print(os.system("ip a | grep 'scope global'"))
    ip = input("Digite seu ip + mascara de sub-rede (ex: /24): ")
    ip_gateway = input("Digite o IP do gateway: ")
    subprocess.run(["sudo", "nmcli", "connection", "modify", rede, "ipv4.method", "manual"])
    subprocess.run(["sudo", "nmcli", "connection", "modify", rede, "ipv4.addresses", ip])
    subprocess.run(["sudo", "nmcli", "connection", "modify", rede, "ipv4.gateway", ip_gateway])
    subprocess.run(["sudo", "nmcli", "connection", "up", rede])
    print("\n Modificação concluida " + "#" * 50)

def ip_automatico():
    print(os.system("nmcli -f name,type,device connection show"))
    rede = input("Digite o nome da sua rede: ")
    subprocess.run(["sudo", "nmcli", "connection", "modify", rede, "ipv4.method", "auto"])
    subprocess.run(["sudo", "nmcli", "connection", "up", rede])
    print("IP dinamico dado!")

if __name__ == "__main__":
    try:
        print("[1] Ligar_wifi")
        print("[2] Desligar_wifi")
        print("[3] Ver_redes")
        print("[4] Conectar_rede_wifi")
        print("[5] configurar IP estatico")
        print("[6] configurar IP automatico")
        option = int(input("Digite a opção: "))
        if option == 1:
            ligar()
        elif option == 2:
            desligar()
        elif option == 3:
            ver_redes()
        elif option == 4:
            conectar_rede()
        elif option == 5:
            ip_estatico()
        elif option == 6:
            ip_automatico()
    except ValueError:
        print("Digite apenas numeros")
