# Biblioteca para manipular data e hora.
from datetime import datetime

# Classe construtora principal de configuração da interface administrativa.
from flask_admin import Admin

# Classe que representa a interface padrão ao acessar a rota `/admin`.
from flask_admin.base import AdminIndexView

# Classe para integrar o MongoDB através do PyMongo junto a
# interface administrativa.
from flask_admin.contrib.pymongo import ModelView

# Função para indicar que é necessário estar logado para acessar a rota.
from flask_simplelogin import login_required

# Biblioteca para trabalhar com formulários a partir do Python.
from wtforms import form, fields, validators

# Conexão com o banco de dados.
from blog.database import mongo

# Apenas para Type Annotation.
from flask import Flask

# Função para gerar slug.
from slugify import slugify

# Monkey Patch para obrigar que o usuário esteja logado antes de acessar
# o painel administrativo.
# `_handle_view` é executado toda vez que a view de admin é chamada.
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
ModelView._handle_view = login_required(ModelView._handle_view)


# Classe para representar o formulário de cadastro/edição dos dados
# dos posts.
class PostsForm(form.Form):
    # Cria um campo do tipo string e obrigatório.
    title = fields.StringField("Title", [validators.data_required()])
    # Cria um campo escondido para armazenar o slug.
    slug = fields.HiddenField("Slug")
    # Campo do tipo textarea para inserir o conteúdo do post.
    content = fields.TextAreaField("Content")
    # Campo para indicar se o post está publicado ou não.
    published = fields.BooleanField("Published", default=True)


# Classe para representar a interface que vai exibir todos os posts do banco
# para os usuários.
class AdminPosts(ModelView):
    # Indica as colunas que vão ser retornadas do banco de dados. O
    # flask admin utiliza esses valores para pesquisar no banco de dados.
    column_list = ("title", "slug", "published", "date")
    # Indica o formulário para essa view, que é o formulário criado
    # anteriormente para o cadastro/edição de posts.
    form = PostsForm

    # Método que é executado toda vez que há uma mudança, como criar um
    # post novo ou editar algum post já existente. Esse método é executado
    # sempre antes de armazenar os dados do post no banco de dados.
    def on_model_change(self, form, post, is_created):
        # Cria o slug a partir do título do post.
        post["slug"] = slugify(text=post["title"])
        # TODO: Verificar se o post com o mesmo slug já existe

        # Verifica se o post está sendo criado pela primeira vez, se estiver
        # é atribuído o momento de criação do mesmo antes de armazenar no
        # banco de dados.
        if is_created:
            post["date"] = datetime.now()


# Função do padrão Application Factory para adicionar a extensão de interface
# administrativa para o app principal.
def configure(app: Flask):
    # Instância e configura a classe responsável pela interface administrativa.
    # Passa o app principal, o nome do app e o template pré-definido
    # a ser utilizado.
    admin = Admin(app, name=app.config["TITLE"], template_mode="bootstrap4")

    # Adiciona a view criada anteriormente a instância do flask-admin, dessa
    # forma a view é de fato exibida para os usuários. É necessário passar
    # a coleção do banco de dados que vai ser usada para coletar os dados e
    # o nome dessa view `Posts`.
    admin.add_view(AdminPosts(coll=mongo.db.get_collection("posts"), name="Posts"))
