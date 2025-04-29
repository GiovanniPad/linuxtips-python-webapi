# Importando a classe do flask para definir a instância da aplicação.
from flask import Flask

# Importando a função para realizar toda a configuração da aplicação.
from blog.config import configure


# Main factory, a partir da onde a aplicação começa.
# Função principal que vai instanciar o app, adicionar configurações
# e no fim retornar o aplicativo.
# O Flask, por padrão, consegue identificar automaticamente essa função.
def create_app():
    # Instanciando o app.
    app = Flask(__name__)
    # Passando as configurações.
    configure(app)
    # Retornando o app.
    return app
