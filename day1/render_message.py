# Biblioteca para se trabalhar com templates
from jinja2 import Environment, FileSystemLoader

# Definindo o ambiente com `Environment` e declarando que o `loader` é
# do tipo `FileSystemLoader`, que são arquivos e que estão localizados
# no caminho `.`.
env = Environment(loader=FileSystemLoader("."))


# Função que pode ser chamada a partir do template, adiciona corações.
# `text` é o texto que vem do template.
def addhearts(text):
    return f"❤️ {text} ❤️"


# Adiciona a funçõa como um filtro que pode ser aplicado no template.
env.filters["addhearts"] = addhearts

# Coleta o template com `get_template` passando o nome dele.
template = env.get_template("email.template.txt")

# Dados fictícios.
data = {
    "name": "Bruno",
    "products": [
        {"name": "iphone", "price": 13000.320},
        {"name": "ferrari", "price": 900000.430},
    ],
    "special_customer": True,
}

# Renderizando o template com os dados fictícios.
# Neste caso é desencompatado um dicionário de dados para que todos os campos
# sejam modificados no template.
print(template.render(**data))
