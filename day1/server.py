# Biblioteca para criar o servidor
import socket

# Criando o servidor usando `socket()`
# `AF_INET` é uma família de endereços e determina qual o
# protocolo de internet utilizado, no caso IPv4.
# `SOCK_STREAM` determina que vai ser utilizado um protocolo baseado
# em conexão. A conexão vai ser estabelecida e as duas partes vão se
# comunicar até a conexão terminar através de uma das partes ou ocorrer
# um erro de rede.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Realiza o processo de `binding`, constroí o endereço completo que vai
# receber as Requests. Esse endereço é composto por um hostname e uma porta.
# Ao construir esse endereço, a porta utiliza fica travada para esse servidor.
# Com isso torna-se possível receber dados.
server.bind(("localhost", 9000))

# Define que o servidor vai passar a escutar qualquer Request para ele,
# ou seja, vai interceptar qualquer Request
# feito ao endereço definido anteriormente,
server.listen()

try:
    while True:
        # Aceita qualquer tipo de Request, retorna uma tupla, onde:
        # `client` é uma referência ao socket da requisição usado
        # para construir uma Response.
        # `address` é o IP do Client e a porta que ele está enviando os dados.
        client, address = server.accept()

        # Coleta os dados da Request do Client, onde:
        # `recv(5000)` determina que o tamanho máximo
        # de uma Request é de 5000 bytes.
        # `decode()` faz o decode de bytes para string (UTF8).
        data = client.recv(5000).decode()

        # Imprime os dados da Request.
        print(f"{data=}", address)

        # Montando e enviando a Response para o Client, onde:
        # `sendall` faz com que o conteúdo da Response
        # seja enviado tudo de uma vez.
        # `encode` converte uma string (UTF8) para bytes para trafegar.
        client.sendall(
            "HTTP/1.0 200 OK\r\n\r\n<html><body>Hello</body></html>\r\n\r\n".encode()
        )

        # Encerra a instância do Client.
        # `SHUT_WR` indica que os próximos envios do socket
        # não serão permitidos, porém o socket
        # ainda pode receber dados/chamadas.
        client.shutdown(socket.SHUT_WR)

except Exception:
    # Fecha o servidor quando houver qualquer tipo de Exceção/Erro.
    server.close()
