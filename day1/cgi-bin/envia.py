#!/usr/bin/env python

# Módulo de interface para processar requisições POST
import cgi

# Coletando todas as informações do formulário
# enviado através de `FieldStorage`.
form = cgi.FieldStorage()

# Coletando o valor do campo `nome`.
nome = form.getvalue("nome")
# Coletando o valor do campo `mensagem`.
mensagem = form.getvalue("mensagem")

# Devolvendo uma resposta com prints.
# Cada linha é um print pois a resposta deve ser um iterável.
# Neste caso, a interface de saída padrão é o navegador.
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Enviado</title>")
print("</head>")
print("<body>")
print("<h1>Enviado com sucesso!</h1>")
print(f"<h2>{nome} - {mensagem}</h2>")
print("</body>")
print("</html>")
