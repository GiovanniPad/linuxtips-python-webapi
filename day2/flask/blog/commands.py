# Biblioteca para a criação de comandos CLI.
import click

# Importando apenas para type annotation.
from flask import Flask

# Importando todos os controllers para criar os comandos CLI respectivos de cada um.
from blog.posts import (
    get_all_posts,
    get_post_by_slug,
    update_post_by_slug,
    new_post,
    unpublish_post_by_slug,
)


# Criando um grupo de comandos. Por padrão, usa o nome da função como nome do grupo.
@click.group()
def post():
    # Documentação curta para o comando.
    """Manage blog posts."""


# Criando um comando dentro do grupo `post`. Por padrão, se não especificar o nome,
# o nome da função é utilizado.
@post.command()
# Especificando que pode ser passado uma opção `--title` para o comando.
@click.option("--title")
# Especificando que pode ser passado uma opção `--content` para o comando.
@click.option("--content")
# Função para criar um novo post no banco de dados.
# As opções criadas anteriormente são passadas como argumentos a esta função.
def new(title, content):
    """Add new post to database."""
    # Invocando a função para criar um novo post passando o título e o conteúdo do post.
    new = new_post(title, content)
    # Imprimindo no terminal a mensagem de confirmação de criação do post.
    click.echo(f"New post created {new}")


# Criando um comando com o nome `list` dentro do grupo de comandos `post`,
# neste caso, o nome do comando é explicitamente informado.
@post.command("list")
# Função para listar todos os posts do banco de dados.
@click.option("--published", type=bool, default=True)
def _list(published: bool):
    """Lists all posts."""
    # Estrutura de repetição exibindo todos os posts.
    for post in get_all_posts(published):
        # Imprimindo os dados do post no terminal.
        click.echo(post)
        # Linha para separar um post do outro.
        click.echo("-" * 30)


# Criando um comando com o nome da função `get` dentro do grupo de comandos `post`.
@post.command()
# Especificando que pode ser passado um argumento ao chamar este comando.
@click.argument("slug")
# Retorna um post com base no slug inserido.
def get(slug):
    """Get post by slug"""
    # Busca o post no banco de dados a partir do slug.
    post = get_post_by_slug(slug)
    # Imprime o post encontrado ou caso não for encontrado, imprime um mensagem informando.
    click.echo(post or "Post not found.")


# Criando um comando com o nome função `update` dentro do grupo de comandos `post`.
@post.command()
# Especificando que pode ser passado um argumento ao chamar este comando.
@click.argument("slug")
# Opção para passar um novo título para o post, é opcional e possui valor padrão `None`
# e tem o seu tipo definido como `string`.
@click.option("--title", default=None, type=str)
# Especificando que pode ser passado uma opção `--content` para o comando, que por padrão
# possui o valor padrão igual a `None` e o seu tipo é `string`.
@click.option("--content", default=None, type=str)
# Especificando que pode ser passado uma opção `--published` para o comando, que por padrão
# possui o valor padrão igual a `None` e o seu tipo é `string`.
@click.option("--published", default=None, type=str)
# Função para modificar um post no banco de dados.
def update(slug, title, content, published):
    """Update post by slug"""
    # Variável de apoio para guardar os novos valores.
    data = {}

    # Verifica se o conteúdo de `title` não está vazio antes de
    # atribuir no dicionário.
    if title is not None:
        data["title"] = title
    # Verifica se o conteúdo de `content` não está vazio antes de
    # atribuir no dicionário.
    if content is not None:
        data["content"] = content
    # Verifica se o conteúdo de `published` não está vazio antes de atribuir
    # no dicionário.
    if published is not None:
        data["published"] = published.lower() == "true"

    # Passando o `slug` para selecionar o post e passando o dicionário
    # com os novos valores.
    update_post_by_slug(slug, data)
    # Mensagem de confirmação que o post foi alterado.
    click.echo("Post updated.")


# Comando para despublicar os posts, será atribuído ao grupo de
# comandos `post`.
@post.command()
# Argumento obrigatório que indica o slug do post a ser despublicado.
@click.argument("slug", required=True)
def unpublish(slug: str):
    """Unpublish post by slug from database."""
    # Chamando a função para despublicar o post através do slug, que é
    # gerado pelo título.
    post_slug = unpublish_post_by_slug(slug)

    # Mensagem de confirmação, indicando que o post foi despublicado.
    click.echo(f"Post `{post_slug}` unpublished.")


# Função de configuração para fazer com que todos esses comandos aparecem no
# `flask shell` desta aplicação.
def configure(app: Flask):
    # Registrando o grupo de comando `post` no Flask Shell.
    app.cli.add_command(post)
