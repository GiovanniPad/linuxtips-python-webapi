# Biblioteca para realizar o build de aplicações Python.
from setuptools import setup

# Função responsável pela configuração do projeto a ser buildado/instalado.
setup(
    # Nome da aplicação.
    name="django_blog",
    # Versão
    version="0.1.0",
    # Pacotes (módulos) necessários e que vão ser instalados no app.
    packages=["djblog", "blog"],
    # Dependências necessárias para executar o app.
    requires=[
        "django",
        "django-markdownify",
    ],
)
