# Variável que disponibiliza as type annotations mais novas para qualquer
# versão do Python 3.
from __future__ import annotations

# Importando a conexão com o banco de dados.
from blog.database import mongo

# Biblioteca para trabalhar com datas e horas.
from datetime import datetime

# Constante para informar que é para ordenar de forma
# descendente e classe para mudar o retorno do `update` do MongoDB.
from pymongo import DESCENDING, ReturnDocument

# Função para gerar slug a partir de um texto.
from slugify import slugify

# Função para emitir exceções do tipo HTTP, com código de status.
from flask import abort


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
def update_post_by_slug(slug: str, data: dict) -> dict | None:
    # Coleta o título do post do dicionário.
    title = data.get("title")

    # Verifica se há um título (texto) e se o valor do slug atual é diferente
    # do slug novo gerado a partir do novo título.
    if title and slug != slugify(title):
        # Realiza a pesquisa no banco de dados para verificar se existe
        # um post com o novo título.
        check_if_title_exist = mongo.db.get_collection("posts").find_one(
            {"slug": slugify(title)}
        )

        # Verifica se retornou algum post com o novo título, se retornou
        # invoca um erro 409 (conflict).
        if check_if_title_exist:
            # Retorna um erro com o código 409 e uma descrição através do `abort`.
            return abort(code=409, description="A post with this title already exists.")
        # Se não existir nenhum post com o novo título, substituir o slug
        # antigo pelo novo slug gerado do título.
        data["slug"] = slugify(title)

    # Pesquisa o documento (post) e atualiza com os novos valores.
    # `ReturnDocument.AFTER` indica que é para retornar o post já com
    # os valores atualizados.
    post = mongo.db.get_collection("posts").find_one_and_update(
        {"slug": slug}, {"$set": data}, return_document=ReturnDocument.AFTER
    )

    # Retorna o post.
    return post


# Função para despublicar (exclusão lógica) um post do banco de dados.
# `slug` é a string que vai ser utilizada para identificação do post.
def unpublish_post_by_slug(slug: str) -> str:
    # Pesquisando o post no banco de dados e atualizando o valor de published
    # para False, indicando que foi despublicado.
    post = mongo.db.get_collection("posts").find_one_and_update(
        {"slug": slug}, {"$set": {"published": False}}
    )

    # Verifica se retornou algo, caso não retornar nada estoura uma exceção.
    if not post:
        # Retornando uma exceção com código 404, indicando que o post não foi
        # encontrado.
        return abort(code=404, description="Post not found.")

    # Retorna o slug do post despublicado.
    return post["slug"]


# Função para criar um novo post.
# `title` indica o título do post.
# `content` indica o conteúdo do post.
# `published` indica se o post está ou não publicado. Por padrão,
# é definido como publicado.
def new_post(title: str, content: str, published: bool = True) -> str:
    # Formata a slug da URL para um formato padrão, todos os caracteres
    # especiais, incluindo ascentos e espaços em brancos (substitui) por `-`.
    slug = slugify(title)

    # Consultando no banco de dados o slug, para ver se o post já existe.
    post = mongo.db.get_collection("posts").find_one({"slug": slug})
    # Caso o post já existir retornar um exceção.
    if post:
        # Retornando um erro 409 (Conflict), dizendo que o post já existe.
        return abort(code=409, description="Post already exists.")

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
