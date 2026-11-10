#!/usr/bin/env python3
# =====================================================================
# AVISO LEGAL:
# Ferramenta de Port Scan (SYN Scan) desenvolvida para fins educacionais
# e testes em ambientes controlados (laboratórios, CTFs ou sua própria rede).
# O uso indevido desta ferramenta para atacar alvos sem autorização
# prévia é ilegal e de inteira responsabilidade do usuário.
# =====================================================================
import time
import threading
import argparse
from scapy.all import IP, TCP, sr1, send
from colorama import Fore, init

init(autoreset=True)

# Trava para evitar que as threads imprimam texto embolado na tela
cadeado = threading.Lock()

def scan(ip, porta):
    # Monta o pacote com flag SYN (S)
    pacote = IP(dst=ip) / TCP(dport=porta, flags="S")

    # Envia e espera 1 segundo pela resposta
    resposta = sr1(pacote, timeout=1, verbose=False)

    if resposta is not None and resposta.haslayer(TCP):
        # SA (SYN-ACK) = Porta Aberta
        if resposta[TCP].flags == "SA":
            with cadeado:
                print(Fore.GREEN + f"[ + ] Porta {porta} está aberta...")
            # Envia um RST para fechar a conexão e não deixar pendurada no alvo
            send(IP(dst=ip) / TCP(dport=porta, flags="R"), verbose=False)

        # RA (RST-ACK) = Porta Fechada
        elif resposta[TCP].flags == "RA":
            with cadeado:
                # Descomente a linha abaixo se quiser ver as portas fechadas
                print(Fore.RED + f"[ - ] Porta {porta} fechada.")
                pass
    else:
        # Se não tiver resposta, a porta provavelmente está filtrada por firewall
        with cadeado:
            print(Fore.YELLOW + f"[ - ] Porta {porta} filtrada ou sem resposta.")
            pass

def iniciar(Alvo, inicio, fim):
    final = fim + 1
    threads = []
    tempo_inicio = time.time() #

    print(Fore.CYAN + f"[*] Iniciando Scan em {Alvo} das portas {inicio} a {fim}...\n")

    try:
        for porta in range(inicio, final):
            t = threading.Thread(target=scan, args=(Alvo, porta), daemon=True)
            threads.append(t)
            t.start()

        # Espera todas as threads finalizarem
        for t in threads:
            t.join()

        tempo_fim = time.time()
        tempo_total = tempo_fim - tempo_inicio
        print(Fore.CYAN + f"\n[*] Script encerrado em {tempo_total:.2f} segundos.")

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Script encerrado com ^C")

def menu():
    p = argparse.ArgumentParser(description="Scan de portas simples via SYN Scan")
    p.add_argument("-p", "--port", required=True, default="0-1000", help="Digite uma faixa de portas (ex: --port 1-1000)")
    p.add_argument("-H", "--host", required=True, default="127.0.0.1", help="Digite o IP ou domínio alvo")
    args = p.parser_args()

    print(Fore.GREEN + f"Alvo: {args.host} \nPort Range: {args.port}")

    # Separa a string do range (ex: "1-1000") e converte para inteiro
    inicio, fim = map(int, args.port.split('-'))
    iniciar(args.host, inicio, fim)

if __name__ == "__main__":
    menu()











