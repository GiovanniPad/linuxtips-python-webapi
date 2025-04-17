# Módulo para tratar requisições POST de formulários.
import cgi

# Variável `conn` para conexão com o servidor.
from database import conn

# Função para trabalhar com caminhos no SO.
from pathlib import Path


# Função para pegar posts no banco de dados.
# `post_id` representa o ID do post.
def get_posts_from_database(post_id=None):
    # Cria um cursor para manipular os dados do banco de dados.
    cursor = conn.cursor()
    # Define os campos desejados da tabela.
    fields = ("id", "title", "content", "author")

    # Se o post for específico, busca o post desejado.
    # Caso contrário, seleciona todos os posts existentes.
    if post_id:
        results = cursor.execute("SELECT * FROM post WHERE id = ?;", post_id)
    else:
        results = cursor.execute("SELECT * FROM post;")

    # Empacota os campos mais os posts utilizando zip,
    # iterando sobre cada post.
    # `zip` pega o primeiro elemento da tupla `fields` e junta com o primeiro
    # elemento da tupla `post` e assim sucessivamente até iterar sobre todos.
    return [dict(zip(fields, post)) for post in results]


# Função para renderizar e retornar o template escolhido.
def render_template(template_name, **context):
    # Coleta o arquivo do template através do caminho e lê o conteúdo
    # usando o `read_text`.
    template = Path(template_name).read_text()
    # Retorna o conteúdo em string do template codificado em `utf-8`.
    return template.format(**context).encode("utf-8")


# Função para retornar uma lista de itens HTML, onde cada item é um post.
def get_post_list(posts):
    # List Comprehension que cria uma lista onde cada item `li` é um post,
    # que contém o `href` (link) e o seu título.
    post_list = [
        f"""<li> <a href='{post["id"]}'> {post["title"]} </a> </li>""" for post in posts
    ]
    # Junta cada item `li` (post) em uma string separando-os
    # por quebra de linha.
    return "\n".join(post_list)


# Função para criar um novo post.
def add_new_post(post):
    # Cria um cursor para inserir um novo registro no banco de dados.
    cursor = conn.cursor()

    # Executa um comando SQL para inserir um novo post no banco de dados.
    # `:title` é uma sintaxe para acessar os dados de um
    # dicionário de parâmetros.
    cursor.execute(
        """\
            INSERT INTO post (title, content, author)
            VALUES (:title, :content, :author)
        """,
        post,
    )
    # Confirma a adição de um novo post no banco de dados.
    conn.commit()


# Função que o servidor WSGI vai chamar (callable).
# `environ` representa todo o ambiente passado pela chamada do cliente.
# `start_response` é a função de callback que vai devolver a resposta.
def application(environ, start_response):
    # Conteúdo do corpo da resposta caso não encontrar nenhuma rota.
    # O conteúdo do corpo deve ser em bytes.
    body = b"Content Not Found"
    # Status code padrão, caso não encontrar nenhuma rota.
    status = "404 Not Found"
    # Definindo o cabeçalho da resposta.
    headers = [("Content-Type", "text/html")]

    # Coletando o caminho/URL (rota) que o usuário está acessando.
    path = environ["PATH_INFO"]
    # Coletando o método HTTP usado para realizar a Request.
    method = environ["REQUEST_METHOD"]

    # Roteamento de rotas/URLs

    # Rota raiz para retornar todos os posts ao usuário.
    if path == "/" and method == "GET":
        # Requisita todos os posts do banco de dados.
        posts = get_posts_from_database()
        # Carrega o template para listar os posts para o usuário.
        # `get_post_list` gera a lista de posts em HTML e passa para
        # a função de renderizar o template.
        body = render_template("list.template.html", post_list=get_post_list(posts))

        # Define o status code de sucesso.
        status = "200 OK"

    # Rota para retornar o post requisitado através da Request.
    elif path.split("/")[-1].isdigit() and method == "GET":
        # Coleta o ID do post a ser exibido.
        post_id = path.split("/")[-1]

        # Renderiza o template de exibir um post no corpo da resposta.
        # `get_posts_from_database` coleta os dados do post em questão,
        # utilizando o ID para realizar a pesquisa.
        body = render_template(
            "post.template.html",
            post=get_posts_from_database(post_id=post_id)[0],
        )

        # Define o código de status como sucesso.
        status = "200 OK"

    # Rota para retornar o formulário de criar um novo post.
    elif path == "/new" and method == "GET":
        # Renderiza o template do formulário no corpo da resposta.
        body = render_template("form.template.html")
        # Define o status de sucesso.
        status = "200 OK"

    # Rota para receber os dados do formulário de criar um novo post e
    # processá-los e adicionar o novo post no banco de dados.
    elif path == "/new" and method == "POST":
        # Coletando os dados do formulário usando cgi.
        # `fp` é o file pointer, que indica da onde os dados estão vindo,
        # neste caso, por usar um servidor WSGI é necessário
        # apontar o `wsgi.input` como origem dos dados.
        # `environ` indica o ambiente, em formato de dicionário.
        # `keep_blank_values` faz com que o cgi mantenha os campos vazios.
        form = cgi.FieldStorage(
            fp=environ["wsgi.input"], environ=environ, keep_blank_values=1
        )

        # Dict Comprehension, cria um dicionário, onde cada par chave-valor
        # representa um input do formulário enviado. A chave sendo o
        # nome do input e o valor é o valor contido no input.
        # `form.list` retorna uma lista de tuplas, onde cada tupla
        # representa um input do formulário.
        post = {item.name: item.value for item in form.list}

        # Invoca a função para adicionar um novo post no banco de dados.
        add_new_post(post)

        # Atribui uma mensagem que o post foi criado ao corpo da resposta.
        body = b"New post created with success!"
        # Status code que indica que o post foi criado com sucesso.
        status = "201 Created"

    # Função de callback que atribui o código de status e o cabeçalho
    # na Response.
    start_response(status, headers)
    # Retorna o corpo em formato de lista (iterável) para a Response.
    return [body]
