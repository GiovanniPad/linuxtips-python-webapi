# Biblioteca para trabalhar com caminhos do OS.
import os

# Classe para inicializar e configurar uma aplicação Flask.
from dynaconf import FlaskDynaconf

# Coletando o caminho absoluto deste arquivo de configuração.
HERE = os.path.dirname(os.path.abspath(__file__))


# Função para configurar todo o aplicativo,
# recebe o `app` que vai ser configurado.
def configure(app):
    # Classe responsável por configurar todo o contexto de configuração
    # da aplicação Flask.
    # `app` é a aplicação que vai ser configurada.
    # `extensions_list` indica a lista contendo todas as extensões/plugins
    # que vão ser usado, buscada por padrão no arquivo de `settings.toml`.
    # `root_path` indica o caminho raiz do arquivo de configuração do projeto,
    # para que a resolução de caminhos possa ser feita.
    FlaskDynaconf(app, extensions_list="EXTENSIONS", root_path=HERE)
