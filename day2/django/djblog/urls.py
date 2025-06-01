# Arquivo para mapear as views com as URLs do projeto.

# Módulo de admin.
from django.contrib import admin
# Função para mapear as views.
from django.urls import path
# Views criadas para serem mapeadas.
from blog.views import new_post, PostDetail, PostList

# Lista de mapeamento de URLs.
urlpatterns = [
    # Mapeia todas as URLs do módulo admin para a URL principal `admin/`.
    path("admin/", admin.site.urls),
    # Mapeia a view `new_post` para a URL `new/`, define um nome para a rota
    # como `new_post` explicitamente. Se não usar, o nome da view é usado.
    path("new/", new_post, name="new_post"),
    # Mapeia a view PostList para a URL raiz `/` (string vazia) e define o nome
    # da view como `index`. Por essa view ser uma classe é necessário invocar a função
    # `as_view()` para definir o ponto de entrada das requisições e respostas.
    path("", PostList.as_view(), name="index"),
    # Mapeia a view PostDetal para a URL `slug/`, na string de URL é definido que
    # a URL vai receber um valor dinâmico, que é o slug de cada post. Essa rota
    # possui o nome `detail` e por ser uma classe, também precisa executar `as_view()`
    # para definir o ponto de entrada das requisições e respostas.
    path("<slug:slug>/", PostDetail.as_view(), name="detail"),
]
