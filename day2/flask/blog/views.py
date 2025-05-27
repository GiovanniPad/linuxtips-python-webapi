# Importando todas as funções e classes necessárias.
from flask import Flask, Blueprint, render_template, abort, request, url_for, redirect

# Decorator responsável por indicar que a view necessita que tenha uma sessão
# autenticada.
from flask_simplelogin import login_required

# Importando todos os controllers.
from blog.posts import get_all_posts, get_post_by_slug, new_post, update_post_by_slug

# Criando um blueprint com o nome `post`. Neste momento esse blueprint
# ainda não faz parte da aplicação principal do Flask.
# `__name__` indica o nome do arquivo para que a resolução
# de caminhos funcione corretamente.
# `template_folder` indica a posta de templates.
bp = Blueprint("post", __name__, template_folder="templates")


# Registra uma rota raiz com o nome `index` no blueprint.
@bp.route("/")
def index():
    # Retorna todos os posts do banco de dados.
    posts = get_all_posts()
    # Renderizada o template `index.html.j2`, responsável
    # por exibir os posts.
    # `posts` é a variável passada no contexto para que os
    # dados possam ser exibidos no template.
    return render_template("index.html.j2", posts=posts)


# Registra uma rota `/<slug>` com o nome `detail` no blueprint.
# Por slug estar entre `<>`, ele é automaticamente passado como
# um parâmetro para a função da rota.
@bp.route("/<slug>")
def detail(slug):
    # Busca e retorna o post do banco de dados, com base no `slug` passado.
    post = get_post_by_slug(slug)
    # Se o post não existir, invoca um erro 404.
    if not post:
        # Função `abort` é responsável por invocar o erro 404, com a mensagem
        # "Post not found.".
        return abort(404, "Post not found.")
    # Caso o post existir, renderizada o template `post.html.j2`, responsável
    # por exibir as informações de um único post.
    # `post` são os dados do post passado dentro do contexto, para que possam
    # ser exibidos no template.
    return render_template("post.html.j2", post=post)


# Registra uma rota `/new` no blueprint, que aceita os métodos GET e POST.
# `login_required` indica que esta view só pode ser acessada se o usuário
# estiver logado.
@bp.route("/new", methods=["GET", "POST"])
@login_required()
def new():
    # Se o método passado for POST, coleta os dados do formulário
    # e cria um novo post no banco de dados.
    if request.method == "POST":
        # Utiliza o objeto `request` para buscar os valores dos campos
        # do formulário, com base em seus `names`.
        title = request.form.get("title")
        content = request.form.get("content")

        # Adiciona o post no banco de dados e retorna o slug dele.
        slug = new_post(title, content)

        # A função `redirect` é usada para redirecionar para outra página/URL.
        # A URL a ser usada vai ser criada invocando a rota `detail` do
        # blueprint `post`, passando o slug do post criado anteriormente.
        # Dessa forma, o post que acaba de ser criado vai ser exibido logo
        # em seguida.
        return redirect(url_for("post.detail", slug=slug))

    # Caso não for o método POST, renderizada o formulário `form.html.j2`,
    # para a criação de um novo post.
    return render_template("form.html.j2")


# Rota para atualizar os dados de um post, esta mesmo rota também invoca
# o formulário responsável pela atualização com os dados atuais. Por isso
# ela aceita ambos métodos GET e POST.
@bp.route("/edit", methods=["GET", "POST"])
def update():
    # Se o método for do tipo POST, então é para processar os novos dados e
    # atualizar o post no banco de dados.
    if request.method == "POST":
        # Coletando os dados do formulário enviado e criando um objeto
        # de apoio.
        new_data = {}
        title = request.form.get("title")
        content = request.form.get("content")
        slug = request.form.get("slug")

        # Verifica se o título é vazio, pois o título não pode ser uma string
        # vazia. Caso for vazia retorna um erro 400.
        if len(title) == 0:
            # Retornando o erro 400 com sua descripção usando a função `abort`.
            return abort(code=400, description="Title must not be empty.")

        # Atribuindo os dados atualizados para a variável de novos dados.
        new_data["title"] = title
        new_data["content"] = content

        # Atualizando o post com os novos dados inseridos.
        post = update_post_by_slug(slug, new_data)

        # Verificando se a operação de atualizar os dados do post foi um
        # sucesso, caso contrário, retorna um erro de código 400.
        if not post:
            # Retornando um erro de código 400 com a descrição usando `abort`.
            return abort(code=400, description="Post not updated.")

        # Redirecionando, no final, para a rota `detail` para exibir o post
        # com as informações atualizadas. A URL usada para redicionar é criada
        # com a função `url_for` e o redirecionamento é feito com `redirect`.
        return redirect(url_for("post.detail", slug=post.get("slug")))

    # Caso a requisição for do tipo GET, vai coletar o valor do slug a partir
    # da query string.
    slug = request.args.get("slug")

    # Pesquisar o post no banco de dados.
    post = get_post_by_slug(slug)

    # Renderizado o template do formulário de atualização do post, passando
    # no contexto os dados do post na variável `post`.
    return render_template("form.html.j2", post=post)


# Função factory para adicionar as views (blueprint) na aplicação principal.
def configure(app: Flask):
    # Registra o blueprint `bp` na aplicação, dessa forma as rotas criadas
    # vão ficar disponíveis na aplicação para os usuários.
    app.register_blueprint(bp)
