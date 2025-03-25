# Carregar os dados
# Dados fictícios
dados = [
    {"nome": "Giovanni", "cidade": "Conchal"},
    {"nome": "Guido", "cidade": "Amsterdan"},
]

# Processar os dados
# Criando um template HTML com placeholders para os dados.
template = """\
<html>
<body>
    <ul>
        <li> Nome: {dados[nome]} </li>
        <li> Cidade: {dados[cidade]} </li>
    </ul>
</body>
</html>
"""

# Renderizar resposta
# Imprimindo na tela o código HTML com os dados inseridos.
for item in dados:
    print(template.format(dados=item))