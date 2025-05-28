# biblioteca para criar comandos no terminal.
import click

# Conexão com o banco de dados.
from blog.database import mongo

# Funções para gerar senhas criptografadas (hashes) e verificar se é uma
# senha válida.
from werkzeug.security import generate_password_hash, check_password_hash

# Extensão para trabalhar com login por sessão no flask.
from flask_simplelogin import SimpleLogin

# Apenas para type annotation.
from flask import Flask


# Função para criar um usuário no banco de dados, com a senha criptografada.
def create_user(**data):
    """Creates user with encrypted password."""

    # Verifica se o nome de usuário e a senha estão presentes, pois são
    # obrigatórias.
    if "username" not in data or "password" not in data:
        # Invoca um erro se alguma das informações não estiver presente.
        raise ValueError("username and password are required.")

    # Substitui a senha inserida pelo usuário por uma versão com criptografia
    # da mesma senha. Usa o método `scrypt` para gerar o hash.
    data["password"] = generate_password_hash(data.pop("password"), method="scrypt")

    # TODO: Verificar se o usuário já existe

    # Cria o novo usuário no banco de dados.
    mongo.db.get_collection("users").insert_one(data)

    # Retorna os dados do usuário criado.
    return data


# Função para validar o login toda vez que o usuário tentar realizá-lo.
def validate_login(user):
    """Validates user login."""

    # Verifica se o nome de usuário e a senha estão presentes, pois são
    # obrigatórias.
    if "username" not in user or "password" not in user:
        # Invoca um erro se alguma das informações não estiver presente.
        raise ValueError("username and password are required.")

    # Pesquisa no banco de dados pelo o usuário inserido.
    db_user = mongo.db.get_collection("users").find_one({"username": user["username"]})

    # Verifica se retornou algum usuário válido e se a senha passada é igual
    # a senha criptografada (hash) armazenada no banco de dados.
    if db_user and check_password_hash(db_user["password"], user["password"]):
        # Retorna True para indicar que o login e os dados são válidos.
        return True
    # Retorna False para indicar que os dados de login são inválidos.
    return False


# Função (padrão Application Factory) para adicionar a parte de login a
# aplicação Flask principal. Recebe `app` que é a aplicação principal.
def configure(app: Flask):
    # Instância a classe da extensão de login do flass, passando o app
    # principal e a função responsável por validar toda tentativa de login.
    SimpleLogin(app=app, login_checker=validate_login)

    # Cria um novo comando no shell do flask.
    @app.cli.command()
    # Indica que o comando pode receber um argumento chamado `username`.
    @click.argument("username")
    # Adiciona um campo para inserir uma senha de uma forma que a senha não
    # apareça no terminal, ao digitar.
    @click.password_option()
    # Função executada ao chamar o comando no shell do flask (add-user).
    # Recebe o nome do usuário e a senha.
    def add_user(username, password):
        """Creates a new user"""
        # Cria um novo usuário com seu nome de usuário e senha e armazena
        # no banco de dados.
        user = create_user(username=username, password=password)
        # Mensagem informando que o usuário foi criado com sucesso.
        click.echo(f"User created {user['username']}")
