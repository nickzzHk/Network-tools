#!/usr/bin/env python3
# =====================================================================
# AVISO LEGAL:
# Este script foi desenvolvido estritamente para fins educacionais 
# e testes em ambientes controlados.
# =====================================================================
from scapy.all import *
from colorama import Fore, init
import argparse

init(autoreset=True)

def processar_mdns(pacote):
    if pacote.haslayer(DNS) and pacote[DNS].qr == 1:
        try:
            if pacote[DNS].an:
                nome = pacote[DNS].an.rrname.decode('utf-8').strip('.')
            else:
                nome = pacote[DNS].qd.qname.decode('utf-8').strip('.')
                
            ip = pacote[IP].src
            
            if len(nome) < 50: 
                print(Fore.GREEN + f"[+] Dispositivo Encontrado: {ip} | Nome: {nome}")
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="mDNS Sniffer (Educacional)")
    parser.add_argument("-if", "--interface", default="wlan0", help="Interface de rede (padrão: wlan0)")
    args = parser.parse_args()

    print(Fore.CYAN + "[*] Escutando tráfego mDNS (UDP 5353)...")
    print(Fore.YELLOW + "[!] Pressione Ctrl+C para parar.\n")

    try:
        sniff(iface=args.interface, filter="udp port 5353", prn=processar_mdns, store=0)
    except KeyboardInterrupt:
        print(Fore.GREEN + "\n[+] Sniffer finalizado.")

if __name__ == "__main__":
    main()
