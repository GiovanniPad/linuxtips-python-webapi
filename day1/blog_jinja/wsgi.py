# Módulo do framework.
from joe import Joe

# Módulo para conectar ao banco de dados.
from database import conn

# Instanciando o app principal do framework.
app = Joe()


# Definindo a rota para listar todos os posts.
# O primeiro argumento é a Regular expression para definir a rota.
# O segundo argumento é o caminho e nome do template.
@app.route(r"^/$", template="list.template.html")
def post_list():
    # Coleta todos os posts do banco de dados.
    posts = get_posts_from_database()
    # Retorna a lista de posts para o template.
    return {"post_list": posts}


# Rota para retonra todos os posts no formato JSON para comunicar com APIs.
# O primeiro argumento é a Regular expression para definir a rota.
# O segundo argumento é o caminho e nome do template.
@app.route("^/api$")
def post_list_api():
    # Coleta todos os posts do banco de dados.
    posts = get_posts_from_database()
    # Retorna a lista de posts e indica que é no formato JSON.
    return {"post_list": posts}, "200 OK", "application/json"


# Definindo a rota para exibir as informações de um único post.
# O primeiro argumento é a Regular expression para definir a rota.
# O segundo argumento é o caminho e nome do template.
@app.route(r"^/(?P<id>\d{1,})$", template="post.template.html")
def post_detail(id):
    # Coleta o post a ser exibido através do ID dele, passado pela função.
    post = get_posts_from_database(post_id=id)[0]
    # Retorna os dados do post para o template.
    return {"post": post}


# Rota apenas para exibir o formulário para adicionar um post.
# O primeiro argumento é a Regular expression para definir a rota.
# O segundo argumento é o caminho e nome do template.
@app.route(r"^/new$", template="form.template.html")
def new_post_form():
    # Retorna nada, pois é apenas para renderizar o template.
    return {}


# Rota para processar os dados enviados através do formulário e
# criar um novo post no banco de dados.
# O primeiro argumento é a Regular expression para definir a rota.
# O segundo argumento é o caminho e nome do template.
@app.route(r"^/new$", method="POST")
def new_post_add(form):
    # Converte os dados do formulário em um dicionário usando
    # dict comprehension.
    post = {item.name: item.value for item in form.list}
    # Cria o novo post no banco de dados.
    add_new_post(post)
    # Retorna a mensagem de sucesso indicado que é texto puro.
    return "New post created with success!", "201 Created", "text/plain"


# Controllers


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


# Executa indefinidamente o servidor wsgi.
if __name__ == "__main__":
    # Função para executar o servidor WSGI em loop.
    app.run()
