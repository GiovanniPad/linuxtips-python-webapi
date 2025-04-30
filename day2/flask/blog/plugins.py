# Biblioteca para rendizar texto Markdown em HTML.
from mistune import markdown

# Importando apenas para type annotation
from flask import Flask


# Função factory para adicionar os plugins a aplicação principal.
def configure(app: Flask):
    # Adiciona a função `markdown` como uma função global para todos os templates.
    app.add_template_global(markdown)
    # Cria uma função lambda para formatar a data usando `strftime`e faz
    # dessa função um filtro para templates com o nome `format_date`.
    app.add_template_filter(lambda date: date.strftime("%d/%m/%Y"), "format_date")
