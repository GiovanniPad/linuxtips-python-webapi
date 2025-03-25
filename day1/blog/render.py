# Biblioteca para manipular caminhos do SO.
from pathlib import Path
# Conexão com o banco de dados.
from database import conn

# 1. Obter os dados
# Criar o cursor para manipular os dados.
cursor = conn.cursor()
# Define os campos desejados da tabela.
fields = ("id", "title", "content", "author")
# Realiza uma query de consulta, selecionando todos os posts.
# `fetchall` transforma o resultado em uma lista.
results = cursor.execute("SELECT * FROM post;").fetchall()

# Empacota os campos + os posts utilizando zip, iterando sobre cada post.
# `zip` pega o primeiro elemento da tupla `fields` e junta com o primeiro
# elemento da tupla `post` e assim sucessivamente até iterar sobre todos.
posts = [dict(zip(fields, post)) for post in results]

# 2. Criar a pasta de destino do site
# Define o caminho da pasta para armazenar os arquivos HTML.
site_dir = Path("site")
# Cria a pasta, caso não existir.
site_dir.mkdir(exist_ok=True)

# 3. Criar uma função para gerar a url com slug
# Função para criar uma url a partir de dados existentes (slug).
def get_post_url(post):
    # `lower` converte tudo para minúsculo.
    # `replace` substitui espaços em branco por "-".
    slug = post["title"].lower().replace(" ", "-")
    return f"{slug}.html"
 
# 4. Renderizar a página index.html
# Acessa através de `Path` o arquivo de template do index.
# `read_text` abre o arquivo, lê todo o conteúdo e fecha.
index_template = Path("list.template.html").read_text()
# Define o caminho aonde o arquivo HTML final vai ser armazenado,
# após, cria o arquivo HTML no caminho especificado.
index_page = site_dir / Path("index.html")

# List Comprehension parar criar os itens da lista a partir de cada post.
# Usando a função `get_post_url` para gerar a URL de acesso.
post_list = [
    f"<li> <a href='{get_post_url(post)}'> {post['title']} </a> </li>"
    for post in posts
]

# Utiliza o método `write_text` para abrir o arquivo, escreve todo o
# conteúdo no arquivo e fecha.
# É possível utilizar o String Format `format` para inserir os dados.
index_page.write_text(
    index_template.format(post_list="\n".join(post_list))
)

# 5. Renderizar as páginas do blog
# Para cada post dos posts
for post in posts:
    # Acessa o template dos posts com `Path` e lê todo o conteúdo de texto
    # do arquivo usando `read_text`.
    post_template = Path("post.template.html").read_text()
    
    # Define o caminho aonde o arquivo HTML final vai ser armazenado,
    # após, cria o arquivo HTML no caminho especificado.
    post_page = site_dir / Path(get_post_url(post))

    # `write_text` escreve o texto do template HTML com os dados já inseridos.
    post_page.write_text(post_template.format(post=post))

# Mensagem de sucesso.
print("Site generated!!!")

# Fecha a conexão com o banco de dados.
conn.close()
