# Função para empacotar e tornar o app executável.
from setuptools import setup

# Só é necessário chamá-la para configurar o executável.
setup(
    # Nome do pacote a ser criado.
    name="flask-blog",
    # Versão do pacote.
    version="0.1.0",
    # Indica os pacotes necessários (dependências).
    packages=["blog"],
    # Bibliotecas necessárias para que funcione.
    install_requires=[
        "flask",
        "flask-pymongo",
        "dynaconf",
        "bootstrap-flask",
        "mistune",
        "python-slugify",
    ],
)
