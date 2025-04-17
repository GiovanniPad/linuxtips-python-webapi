# Biblioteca para manipular Regular Expressions (Expressões regulares).
import re

# Biblioteca para coletar os valores dos campos de inputs de formulários
# enviados pelo método POST.
import cgi

# Biblioteca para trabalhar com o formato de arquivo JSON.
import json

# Biblioteca para trabalhar com templates.
# `Environment` define o ambiente.
# `FileSystemLoader` define o tipo de template, no caso, um arquivo.
from jinja2 import Environment, FileSystemLoader

# Função para criar um servidor WSGI simples.
from wsgiref.simple_server import make_server


# Classe principal do framework, representa tudo.
class Joe:
    # Função construtora, vai ser executada ao instanciar.
    # `self` é porque ela recebe a própria instância da classe,
    # dessa forma consegue acessar os dados internos dela.
    # `template_folder` é a pasta que estão os templates,
    # por padrão usa `templates`
    def __init__(self, template_folder="templates"):
        # Define a lista do mapeamento das URLs, contém todas os
        # endpoints nesta lista.
        self.url_map = []
        # Define a pasta que está os templates.
        self.template_folder = template_folder
        # Define o ambiente para carregar os templates usando `Environment` e
        # atribui um loader para indicar que vai ser renderizado arquivos
        # com `FileSystemLoader`.
        self.env = Environment(loader=FileSystemLoader(template_folder))

    # Método para registrar rotas.
    # `self` é porque ela recebe a própria instância da classe.
    # `rule` é a regra em expressão regular para indicar o caminho.
    # `method` indica o método HTTP.
    # `template` indica o template a ser usado, por padrão, nenhum.
    def route(self, rule, method="GET", template=None):
        # Cria uma função decorator que vai envolver a função `view`,
        # que é a função responsável por processar os dados da requisição e
        # devolver a resposta ao cliente.
        def decorator(view):
            # Adiciona a rota para a lista de rotas, registrando-a.
            self.url_map.append((rule, method, view, template))
            # Retorna a própria função para continuar a execução.
            return view

        # Retorna o decorator para que continue a execução.
        return decorator

    # Função para renderizar e retornar o template escolhido.
    # `self` é porque ela recebe a própria instância da classe.
    # `template_name` é o nome do template a renderizar.
    # `**context` é um dicionário contendo todos os dados que o template
    # precisa exibir. Realiza o desempacotamento dele ao executar.
    def render_template(self, template_name, **context):
        # Coleta o template através do ambiente passando o nome dele.
        template = self.env.get_template(template_name)
        # Retorna o template renderizado e formatado em bytes com o encode
        # de UTF-8.
        return template.render(**context).encode("utf-8")

    # Método especial para tornar a classe callable ou chamável/executável.
    # `self` é porque ela recebe a própria instância da classe.
    # `environ` representa todo ambiente.
    # `start_response` é a função de callback para devolver a resposta.
    def __call__(self, environ, start_response):
        # Conteúdo do corpo da resposta caso não encontrar nenhuma rota.
        # O conteúdo do corpo deve ser em bytes.
        body = b"Content Not Found"
        # Status code padrão, caso não encontrar nenhuma rota.
        status = "404 Not Found"
        # Definindo o tipo padrão de retorno de conteúdo.
        ctype = "text/html"
        # Coletando o caminho/URL (rota) que o usuário está acessando.
        path = environ["PATH_INFO"]
        # Coletando o método HTTP usado para realizar a Request.
        request_method = environ["REQUEST_METHOD"]

        # Resolvendo URLs
        # Desempacota cada URL registrada na lista de URLs.
        for rule, method, view, template in self.url_map:
            # Verifica se a regra bate com o caminho solicitado, se não for
            # não executa nada e passa para a próxima iteração.
            if match := re.match(rule, path):
                # Se o método usado for diferente do passado, continuar
                # para a próxima iteração.
                if method != request_method:
                    continue

                # Coletar os argumentos passados através
                # da URL com o `match.groupdict`.
                view_args = match.groupdict()

                # Verifica se o método é do tipo POST, se for
                # atribui os dados do formulário para o resultado.
                if method == "POST":
                    # Coleta todos os valores de cada input do formulário enviado.
                    # `fp` indica de onde os dados estão vindo.
                    # `environ` indica todo o ambiente do navegador passado.
                    # `keep_blank_values` indica que é para manter
                    # os campos vazios.
                    view_args["form"] = cgi.FieldStorage(
                        fp=environ["wsgi.input"], environ=environ, keep_blank_values=1
                    )

                # Passa todos os argumentos para a função que vai
                # processá-los e então coleta a resposta do cliente
                # em `view_result`.
                view_result = view(**view_args)

                # Se o resultado for uma instância de tupla,
                # apenas desempacota. Aqui indica que é texto puro.
                if isinstance(view_result, tuple):
                    # Desempacotamento tupla.
                    view_result, status, ctype = view_result
                # Se não for uma tupla, retorna o status code como 200 OK.
                else:
                    status = "200 OK"

                # Renderiza o template se ele for passado.
                if template:
                    # Renderiza o template no `body` da resposta, passando
                    # os dados a serem carregados e o nome do template.
                    body = self.render_template(template, **view_result)

                # Verifica se o resultado do processamento é um dicionário
                # e o tipo do conteúdo a ser exibido é JSON, caso for retorna
                # um JSON como resposta.
                elif isinstance(view_result, dict) and ctype == "application/json":
                    # Convertendo o dicionário para JSON e encodando para bytes
                    # no formato UTF-8.
                    body = json.dumps(view_result).encode("utf-8")
                else:
                    # Caso não for JSON, apenas retorna uma string encodificada
                    # no padrão UTF-8.
                    body = str(view_result).encode("utf-8")

        # Definindo o cabeçalho da resposta, com o tipo de conteúdo dinâmico.
        headers = [("Content-Type", ctype)]
        # Função de callback que atribui o código de status e o cabeçalho
        # na Response.
        start_response(status, headers)
        # Retorna o corpo em formato de lista (iterável) para a Response.
        return [body]

    # Método para executar indefinidamente o servidor WSGI.
    # `self` é porque ela recebe a própria instância da classe.
    # `host` indica o hostname (IP ou Domain Name).
    # `port` indica a porta lógica a ser escutada.
    def run(self, host="0.0.0.0", port=8000):
        # Cria um servidor simples WSGI, passando o hostname, a porta e
        # a função de callback é a própria instância da classe do framework.
        server = make_server(host, port, self)
        # Executa o servidor WSGI em loop infinito.
        server.serve_forever()
