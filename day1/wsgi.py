# Deve usar um objeto callable
# environ, start_response (callback)
# return iterável

# Definindo a função que vai ser chamada pelo servidor WSGI.
# `environ` representa todo o ambiente passado pela chamada do cliente.
# `start_response` é a função de callback que vai devolver a resposta.
def application(environ, start_response):
    # Montando a Resposta (Response).

    # Status code da resposta.
    status = "200 OK"
    # Define os cabeçalhos da resposta.
    headers = [("Content-type", "text/html")]
    # Define o corpo da resposta.
    # O corpo deve ser em bytes e não em string.
    body = b"<strong>Hello World!!!</strong>"
    # chamando a função de callback passando o status code e os cabeçalhos.
    start_response(status, headers)
    # Retornando o corpo da resposta.
    # O retorno é uma lista pois é necessário ser um iterável.
    return [body]


# Abre um servidor WSGI pré embutido no Python.
if __name__ == "__main__":
    # Importa o método para criar o servidor.
    from wsgiref.simple_server import make_server
    # Abre o servidor, escutando qualquer chamada e na porta 8000,
    # passando a função application que vai tratar as chamadas.
    server = make_server("0.0.0.0", 8000, application)
    # Loop infinito para servir o servidor para sempre.
    server.serve_forever()
