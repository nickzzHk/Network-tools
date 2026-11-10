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

        if not enviar:
            print("Nenhum dispositivo encontrado na rede, ou (IP/masca>
            return

        print(Fore.GREEN + Style.BRIGHT + "[--- IP ---]\t\t[--- MAC -->
        for enviado, recebido in enviar:
            ip_receb = recebido.psrc
            mac_receb = recebido.hwsrc
            print(ip_receb + "\t\t" + mac_receb)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "Scan encerrado por ^C")

    except PermissionError:
        print(Fore.RED + "Precisa de permissão root para rodar arquivo>

    except Exception as e:
        print(Fore.RED + f"Ocorreu um erro inesperado: {e}")

    finally:
       fim = time.time() - inicio
       print(Fore.YELLOW + Style.BRIGHT + f"Scan completo em {fim:.2f}>

def menu():

    p = argparse.ArgumentParser(
           description="Scan de rede"
                               )
    p.add_argument("-i", "--ip", required=True, help="Digite o IP (ex:>
    p.add_argument("-m", "--masq", required=True, help="Digite sua mas>

    args = p.parse_args()
    print(f"Iniciando scan em: {args.ip}")
    scanear_rede(args.ip, args.masq)

menu()