import argparse
import time
from scapy.all import Ether, srp, ARP
from colorama import Style, Fore, init
init(autoreset=True)

def scanear_rede(ip, mascara):
    inicio = time.time()
    destino = ip + mascara
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, pdst=destino)
    try:
        enviar, _ = srp(pkt, timeout=5, verbose=False)
        print(Fore.GREEN + Style.BRIGHT + "[--- IP ---]\t\t[--- MAC ---]")
        for enviado, recebido in enviar:
            ip_receb = recebido.psrc
            mac_receb = recebido.hwsrc
            print(ip_receb + "\t\t" + mac_receb)
    finally:
       fim = time.time() - inicio
       print(Fore.YELLOW + Style.BRIGHT + f"Scan completo em {fim:.2f}")

def menu():

    p = argparse.ArgumentParser(
           description="Scan de rede"
                               )
    p.add_argument("-i", "--ip", help="Digite o IP (ex:192.168.1.0)")
    p.add_argument("-m", "--masq", help="Digite sua mascara de subrede (ex: /24, /25, para saber qual é basta dar um [ip a] em inet você vera seu ip seguido pela mascara")

    args = p.parse_args()
    print(f"Iniciando scan em: {args.ip}")
    scanear_rede(args.ip, args.masq)

menu()
