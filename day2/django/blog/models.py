# Arquivo para definir os models que representa cada tabela.

# Módulo com as funcionalidades necessárias para criar models.
from django.db import models


# Criando o modelo `Post` que representa a tabela de posts no banco de dados.
# Herda de `Model` todas as funcionalidades necessárias.
class Post(models.Model):
    # Cria uma coluna com o nome `title` do tipo text de tamanho máximo de 255.
    title = models.CharField(max_length=255)
    # Cria uma coluna com o nome `slug` do tipo text com tamanho máximo de 255.
    # E ela há a característica de ser única, ou seja, não pode ter valores
    # iguais dessa coluna na tabela. Outra característica especial é que é
    # do tipo slug, com isso ela é tratada de uma forma especial, pois o slug
    # é utilizado para representar cada Post de maneira única e usada para
    # pesquisar por algum post também.
    slug = models.SlugField(max_length=255, unique=True)
    # Coluna com nome `content`, esse campo também é do tipo text, porém ele
    # não possui limite de caracteres máximo por registro. Este campo armazena
    # o conteúdo do post.
    content = models.TextField()
    # Campo de nome `published` do tipo booleano, ele indica se o Post está
    # publicado ou não.
    published = models.BooleanField(default=True)
    # Campo de nome `date` do tipo DateTime (armazena data e hora) ele possui
    # a configuração `auto_now_add` como True, isso faz com que a data e hora
    # da criação de um post (registro) seja definida automaticamente.
    date = models.DateTimeField(auto_now_add=True)

    # Método especial que é usado para definir o que e como a instância vai
    # exibir as informações ao ser passada dentro de um `print`.
    def __str__(self):
        return self.title

    # Subclasse dentro da classe principal, utilizada para definir metadados.
    class Meta:
        # Define que os posts vão ser ordenados em ordem decrescente através
        # da coluna `date`.
        ordering = ["-date"]
