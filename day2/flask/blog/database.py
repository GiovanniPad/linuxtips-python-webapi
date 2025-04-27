# Biblioteca para manipular o banco de dados MongoDB.
from flask_pymongo import PyMongo

# Apenas inicializando a extensão `PyMongo`, por conta de não passar
# o app, ela não poderá ser usada, neste momento. É uma maneira lazy,
# para que o `app` seja passado apenas dentro da função factory.
mongo = PyMongo()

# Função factory para adicionar o `app` na extensão do PyMongo,
# configurando, assim, o banco de dados.
def configure(app):
    mongo.init_app(app)