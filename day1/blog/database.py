# Biblioteca para trabalhar com banco de dados SQLite.
from sqlite3 import connect

# 1. conectar com o banco de dados
# Conecta no banco (cria caso não existir).
conn = connect("blog.db")
# Define um cursor para manipular os dados do banco.
cursor = conn.cursor()

# 2. definir e criar as tabelas
# Executa um comando SQL para criar uma tabela.
conn.execute(
    """\
        CREATE TABLE if not exists post (
            id integer PRIMARY KEY AUTOINCREMENT,
            title varchar UNIQUE NOT NULL,
            content varchar NOT NULL,
            author varchar NOT NULL
        );
    """
)

# 3. Criamos os posts iniciais para alimentar o banco de dados
# Lista de posts para alimentar o banco.
posts = [
    {
        "title": "Python é eleita a linguagem mais popular",
        "content": """\
        A linguagem Python foi eleita a linguagem mais popular pela revista
        tech masters e segue dominando o mundo.
        """,
        "author": "Satoshi Namamoto",
    },
        {
        "title": "Como criar um blog utilizando Python",
        "content": """\
        Neste tutorial você aprenderá como criar um blog utilizando Python.
        <pre> import make_a_blog </pre>
        """,
        "author": "Guido Van Rossum",
    },
]

# 4. Inserimos os posts caso o banco de dados esteja vazio
# Executa uma query de consulta utilizando o cursor.
# `fetchall` faz com que os dados retornados fiquem no formato de lista.
count = cursor.execute("SELECT * FROM post;").fetchall()

# Verifica se o banco de dados está vazio.
if not count:
    # Executa vários comandos em sequência utilizando o cursor.
    cursor.executemany(
        """\
            INSERT INTO post (title, content, author)
            VALUES (:title, :content, :author);
        """,
        posts,
    )
    
    # Realiza o commit das mudanças
    conn.commit()

# 5. Verificamos que foi realmente inserido
# Executa uma query de consulta utilizando o cursor.
# `fetchall` faz com que os dados retornados fiquem no formato de lista.
posts = cursor.execute("SELECT * FROM post;").fetchall()

# Verifica se os posts realmente foram criados.
assert len(posts) >= 2
