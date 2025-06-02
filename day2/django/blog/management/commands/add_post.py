# Criando um comando personalizado dentro da aplicação `blog` para adicionar
# posts ao blog.

# Importa as classes responsáveis por criar o comando e representar um erro.
from django.core.management.base import BaseCommand, CommandError
# Model `Post`
from blog.models import Post
# Função para criar slugs.
from django.utils.text import slugify


# Criando a classe responsável por lidar com o comando, deve, obrigatoriamente
# herdar de `BaseCommand`.
class Command(BaseCommand):
    """Adds new post to the database."""
    # Descrição que vai ser exibida ao usar `--help` no comando.
    help = "Creates a new Post in the database."


    # Método para declarar quais os argumentos que este comando vai receber
    # `parser` é tipo o argparser da biblioteca sys.
    def add_arguments(self, parser):
        # Adiciona um argumento de nome `title` do tipo string e que é
        # obrigatório, este argumento representa o título do post.
        parser.add_argument("--title", type=str, required=True)
        # Declara outro argumento de nome `content` do tipo string e que é
        # obrigatório também, ele representa o conteúdo do post.
        parser.add_argument("--content", type=str, required=True)


    # Método que vai lidar com o processamento de dados do comando, ou seja,
    # é onde é declarado o que o comando vai fazer e como ele vai fazer.
    # `options` é um dicionário que recebe diversas informações, incluindo os
    # valores dos argumentos no formato chave-valor.
    def handle(self, *args, **options):
        # É uma boa prática envolver a ação de um comando em um bloco try
        # para capturar qualquer erro possível.
        try:
            # Tenta criar o Post no banco de dados usando o método `create`
            # do `model` Post, passando os valores dos campos da tabela.
            post = Post.objects.create(
                title=options["title"],
                slug=slugify(options["title"]),
                content=options["content"]
            )
        # Captura qualquer exceção gerada ao tentar criar um novo Post.
        except Exception as e:
            # Invoca um erro padrão para comandos com a mensagem do erro dentro.
            raise CommandError(e)
        # Caso nenhuma exceção ocorrer, vai executar esse bloco.
        else:
            # Imprime no `stdout` (terminal) a mensagem de sucesso, indicando
            # que o Post foi criado com sucesso.
            self.stdout.write(self.style.SUCCESS(
                f"Post '{post.title}' created."
            ))
