# Importando a classe do flask para definir
# a instância da aplicação.
# `url_for` é uma função para coletar as URLs das rotas.
# `request` é o objeto que representa a requisição de um cliente.
from flask import Flask, url_for, request

# Definindo a inst6ancia da aplicação a apartir da classe Flask.
# `__name__` é o nome do arquivo, que representa a aplicação
# que é passada ao parâmetro `import_name`, que é obrigatório e usado
# para resolver os imports de módulos e bibliotecas, assim
# como recursos da aplicação.
app = Flask(__name__)

# Definindo uma variável de configuração no contexto de configuração.
# O dicionário `app.config` contém todas as variáveis e configurações que
# são mantidas quando a aplicação é servida.
app.config["APP_NAME"] = "Meu Blog"


# Definindo uma função para ser executada ao ocorrer o erro 404.
# É uma função de `Error Handler`, ou seja, ela lida com o erro.
@app.errorhandler(404)
def not_found_page(error):
    return f"Not Found on {app.config['APP_NAME']}"


# Outra maneira de registrar a função de `Error Handler`.
# app.register_error_handler(404, not_found_page)


# Definindo uma rota usando um decorator, onde "/" é a regra
# da rota, indicando a rota raiz da aplicação. Não é necessário
# utilizar expressões regulares, pois por baixo dos panos o Flask
# já faz todo esse trabalho.
# `endpoint` indica que o nome dessa rota é `index`, por padrão o Flask
# atribui o nome da rota igual ao nome da função que vai ser executada ao
# fazer uma requisição para a rota. Caso não fosse explicitado, o nome
# da rota seria `hello`.
@app.route("/", endpoint="index")
# Defindo a função que vai ser executada ao chamar a rota acima.
def hello():
    # Coletando e armazenando a URL a partir da função que é executada
    # por essa rota, no caso a função `read_content`.
    # `title` é um parâmetro passado a essa função.
    content_url = url_for("read_content", title="Novidades de 2022")

    # Retornando várias f-string de várias linhas puras contendo HTML,
    # por padrão, o Flask ao identificar uma string pura,
    # ele renderiza como HTML. Neste caso não deve usar vírgulas para
    # separar as linhas, caso usar, o Python vai entender que é uma tupla.
    # O segundo valor passado na tupla de retorno indica o código de
    # status da resposta, caso não for específico, usa 200 por padrão.
    return (
        # Exibe o valor da variável de configuração `APP_NAME` em um título.
        f"<h1>{app.config['APP_NAME']}</h1>"
        # Cria um link apontando para a URL `content_url` adquirida usando
        # `url_for`.
        f"<a href='{content_url}'>Novidades de 2022</a>"
        "<hr>"
        # O objeto `request` contém as informações da requisição HTTP e
        # neste caso, ele está exibindo todos os dados recebidos via
        # query string.
        f"{request.args}"
    ), 201


# Criando uma rota que vai ser executada sempre que houver uma requisição
# na rota `/` seguida de um texto qualquer e esse texto qualquer vai ter
# um nome `title` atribuído a ele e será passado por injeção de dependência
# para a função `read_content` acessá-lo.
@app.route("/<title>")
def read_content(title):
    # Coletando a URL da rota com o nome `index`,
    # explicitada na rota anterior.
    index_url = url_for("index")

    # retornando HTML passando a variável `title` e `index_url` como link.
    return f"<h1>{title}<h1> <a href={index_url}>Voltar</a>"


# Outra maneira de registrar uma rota.
# app.add_url_rule("/<title>", view_func=read_content)
