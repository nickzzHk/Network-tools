#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main() {
    struct sockaddr_in alvo;
    alvo.sin_family = AF_INET;
    alvo.sin_addr.s_addr = inet_addr("127.0.0.1"); 

    for (int porta = 1; porta <= 10000; porta++) {
        // 1. Criar um socket NOVO a cada iteração
        int meu_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (meu_socket == -1) continue; // Se falhar, pula pra próxima

        alvo.sin_port = htons(porta);
        
        // 2. Tentar conectar
        int resultado = connect(meu_socket, (struct sockaddr *)&alvo, sizeof(alvo));

        // 3. Verificar
        if (resultado == 0) {
            printf("[+] Porta %d ABERTA!\n", porta); // Agora mostra a porta certa
        }

        // 4. Fechar o socket (dentro do loop!)
        close(meu_socket);
    }

    return 0;
}
