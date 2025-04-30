# Variável que disponibiliza as type annotations mais novas para qualquer
# versão do Python 3.
from __future__ import annotations

# Importando a conexão com o banco de dados.
from blog.database import mongo

# Biblioteca para trabalhar com datas e horas.
from datetime import datetime

# Constante para informar que é para ordenar de forma
# descendente.
from pymongo import DESCENDING


# Função para retornar todos os posts que estão publicados ou não, por padrão,
# retorna apenas os posts publicados.
# `published` indica se o post está ou não publicado.
def get_all_posts(published: bool = True):
    # Conecta ao banco de dados e acessa a coleção `posts` e busca todos os
    # posts com base na variável `published`.
    posts = mongo.db.get_collection("posts").find({"published": published})
    # Retorna todos os posts, ordenando-os pelo campo `date`
    # de forma descendente.
    return posts.sort("date", DESCENDING)


# Função para retornar um post com base em um slug.
# `slug` indica a string usada para buscar o post no banco de dados.
def get_post_by_slug(slug: str) -> dict:
    # Conecta ao banco de dados e acessa a coleção `posts` e busca todos o
    # post com base no `slug` inserido.
    post = mongo.db.get_collection("posts").find_one({"slug": slug})
    # Retorna o post encontrado.
    return post


# Função para atualizar as informações de um post.
# `slug` indica a string usada para buscar o post no banco de dados.
# `data` indica o dicionário contendo os novos valores para o post.
def update_post_by_slug(slug: str, data: dict) -> dict:
    # TODO: Se o título mudar, atualizar o slug (falhar se já existir).

    # Busca o `post` no banco de dados com base no `slug` inserido e
    # atualiza com as novas informações.
    return mongo.db.get_collection("posts").find_one_and_update(
        {"slug": slug}, {"$set": data}
    )


# Função para criar um novo post.
# `title` indica o título do post.
# `content` indica o conteúdo do post.
# `published` indica se o post está ou não publicado. Por padrão,
# é definido como publicado.
def new_post(title: str, content: str, published: bool = True) -> str:
    # TODO: refatorar a criação do slug, removendo acentos.
    # Formata a slug da URL para um formato padrão, removendo caracteres
    # especiais, espaços e deixando tudo minúsculo.
    slug = title.replace(" ", "-").replace("_", "-").lower()
    # TODO: Verificar se post com este slug já existe.

    # Inserindo um novo documento (post) na coleção `posts`.
    mongo.db.get_collection("posts").insert_one(
        {
            "title": title,
            "content": content,
            "published": published,
            "slug": slug,
            "date": datetime.now(),
        }
    )
    # Retornando o slug do post criado.
    return slug
