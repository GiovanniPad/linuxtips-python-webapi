# Importando a classe do flask para definir
# a instância da aplicação.
from flask import Flask

# Definindo a inst6ancia da aplicação a apartir da classe Flask.
# `__name__` é o nome do arquivo, que representa a aplicação
# que é passada ao parâmetro `import_name`, que é obrigatório e usado
# para resolver os imports de módulos e bibliotecas, assim
# como recursos da aplicação.
app = Flask(__name__)


# Definindo uma rota usando um decorator, onde "/" é a regra
# da rota, indicando a rota raiz da aplicação. Não é necessário
# utilizar expressões regulares, pois por baixo dos panos o Flask
# já faz todo esse trabalho.
@app.route("/")
# Defindo a função que vai ser executada ao chamar a rota acima.
def hello():
    # Simulando um erro.
    # 1 / 0
    # Retornando uma string pura contendo HTML, por padrão, o Flask
    # ao identificar uma string pura, ele renderiza como HTML.
    # O segundo valor passado na tupla de retorno indica o código de
    # status da resposta, caso não for específico, usa 200 por padrão.
    return "<strong>Hello, World!</strong>", 201
