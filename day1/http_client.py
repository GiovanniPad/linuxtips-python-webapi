# Biblioteca para criar um socket.
import socket

# Um cliente é definido através de `socket()`.
# `AF_INET` é uma família de endereços e determina qual o
# protocolo de internet utilizado, no caso IPv4.
# `SOCK_STREAM` determina que vai ser utilizado um protocolo baseado
# em conexão. A conexão vai ser estabelecida e as duas partes vão se
# comunicar até a conexão terminar através de uma das partes ou ocorrer
# um erro de rede.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Realiza e estabelece uma conexão com o servidor (endereço)
# `example.com`, na porta 80.
client.connect(("example.com", 80))

# Monta o texto da Request especificando o método HTTP, a URL e o recurso e
# por fim, indicando qual a versão e protocolo utilizado, no caso o HTTP 1.0
# `encode` garante que a string estará em bytes no formato UTF-8.
cmd = "GET http://example.com/index.html HTTP/1.0\r\n\r\n".encode()

# Envia a Request para a conexão estabelecida.
client.send(cmd)

while True:
    # Recebe a Response do servidor com um limite de 512 bytes por loop,
    # dessa forma o desempenho não é afetado por ter de carregar todo o recurso
    # de uma única vez
    data = client.recv(512)

    # Verifica se a Response está completa e encerra o loop.
    if len(data) < 1:
        break

    # Imprime os resultados.
    # `decode()` converte de bytes para string no formato UTF-8.
    print(data.decode(), end="")

# Fecha a conexão com o servidor no final.
client.close()
