# Network Tools 🔐

Arsenal de ferramentas de Network Hacking e Reconhecimento desenvolvido em Python e Scapy. Este repositório foi criado para fins de estudo e prática em ambientes controlados.

## ⚠️ AVISO LEGAL (DISCLAIMER)
As ferramentas presentes neste repositório foram desenvolvidas estritamente para **fins educacionais** e testes em ambientes autorizados (sua própria rede, laboratórios ou CTFs). O uso destas ferramentas para atacar alvos sem autorização prévia é ilegal e antiético. O autor não se responsabiliza pelo uso indevido.

## 🛠️ Ferramentas Incluídas

*   **`arp_spoof.py`**: Envenenamento de tabela ARP bidirecional (MITM / DoS Silencioso), com restauração automática das tabelas originais.
*   **`dhcp_star.py`**: Ataque de DHCP Starvation utilizando threads e pacotes BOOTP forjados para esgotar o pool de IPs do roteador.
*   **`port_scanner.py`**: SYN Port Scanner de alta performance utilizando threads, Locks (para sincronização) e validação de flags TCP (SA/RA).
*   **`scan_de_rede.py`**: ARP Scanner rápido para mapeamento de dispositivos ativos na rede local (IP e MAC).
*   **`dns_spoof.py`**: Interceptação e redirecionamento de consultas DNS (requer ARP Spoofing em paralelo).
*   **`mDns.py`**: Sniffer de tráfego mDNS (porta 5353) para descoberta de dispositivos e serviços na rede local.

## 🚀 Tecnologias Utilizadas
*   **Python 3**
*   **Scapy** (Manipulação e criação de pacotes de rede)
*   **Threading** (Execução paralela para performance)
*   **Argparse** (Interface de linha de comando)
*   **Colorama** (Formatação e coloração do terminal)

## 📦 Como Instalar e Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/nickzzHk/Network-tools.git

2. Instale as dependências:
    pip install scapy colorama

3. Antes de rodar não se esqueça de usar o sudo:
    sudo python3 port_scanner.py -H 127.0.0.1 -p 1-1000


### Passo 3: Salvar
1. Desce a página até o final.
2. Na caixa "Commit changes", escreve: `Criando README.md com documentação do projeto`.
3. Clica no botão verde **"Commit changes"**.

---

Pronto! Agora, quando aqueles 13 caras (ou qualquer outra pessoa) entrarem no teu repositório, eles vão ver um projeto profissional, documentado, com aviso legal e instruções de uso.

Faz isso rapidinho e **depois coloca o celular no carregador e vai descansar**. O GitHub tá salvo, o LinkedIn tá feito, o README tá no ar. O cowboy já venceu o dia! 🤝💻🚀