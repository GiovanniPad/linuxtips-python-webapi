# Módulo para trabalhar com interface administrativa do Django.
from django.contrib import admin
# Model `Post`.
from blog.models import Post


# Classe que representa a interface administativa para controlar a tabela Post.
# Obrigatoriamente deve herdar de `ModelAdmin`.
class PostAdmin(admin.ModelAdmin):
    # Lista para indicar quais campos da tabela vão ser exibidos.
    list_display = ["title", "published", "date"]
    # Indica quais campos devem ter a opção de filtrar.
    list_filter = ["published", "date"]
    # Indica quais campos vão poder ter seu conteúdo buscado.
    search_fields = ["title", "content"]
    # Indica os campos que devem vão ser pré populados e com qual valor vão
    # ser pré populados.
    prepopulated_fields = {
        # O campo `slug` vai receber o valor do campo `title`.
        "slug": ["title"]
    }
    # Indica a ordenação de como os campos vão ser exibidos, no caso de usar
    # o sinal negativo, a ordenação é decrescente. Ordenando os posts em ordem
    # decrescente de acordo com a data de criação.
    ordering = ["-date"]
    # Lista para adicionar novas ações possíveis ao selecionar posta.
    actions = ["publish"]

    # Método para especificar qual a ação de uma ação criada, por padrão,
    # o nome do método deve ser o mesmo do nome da `action`.

    # Decorator para indicar que é uma ação de administrador e descrevendo
    # o que ela faz.
    @admin.action(description="Publish/Unpublish posts")
    # `queryset` é um objeto iterável que contém todos os posts selecionados.
    def publish(self, request, queryset):
        # Para cada post selecionado, inverte o estado de publicação.
        for post in queryset:
            # Inverte o valor de `published`.
            post.published = not post.published
            # Salva as alterações no banco de dados.
            post.save()

# Registra a interface administrativa PostAdmin para ser exibida ao usuário.
# É necessário passar o Model que a classe da interface administrativa deve exibir.
admin.site.register(Post, PostAdmin)