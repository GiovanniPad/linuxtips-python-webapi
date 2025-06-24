# Arquivo para definir as views do app `blog`.

# Decorator para indicar que determinada view só pode ser acessada caso o
# usuário estiver logado.
from django.contrib.auth.decorators import login_required

# Classe para definir um formulário de um model.
from django.forms import ModelForm

# Classe para realizar o redirecionamento (response) nas views.
from django.http import HttpResponseRedirect

# Função para renderizar templates.
from django.shortcuts import render

# Função para retornar o caminho de uma view.
from django.urls import reverse

# Função para gerar slugs.
from django.utils.text import slugify

# Views genéricas.
from django.views.generic import ListView, DetailView

# Model do Post.
from blog.models import Post


# Cria a classe que representa o formulário do model Post. Herda de `ModelForm`
# todas as funcionalidades necessárias.
class PostForm(ModelForm):
    # Classe para metadados.
    class Meta:
        # Indica que este formulário está atrelado ao model `Post`.
        model = Post
        # Indica quais campos do model vão aparecer no formulário.
        fields = ["title", "content", "published"]


# Function view, view criada no formato de função, representa a view para
# criar novos posts.
# `request` é o objeto que recebe todas as informações da requisição.
# `login_required` decorator que indica que a view precisa de autenticação
# para acessar.
@login_required
def new_post(request):
    # Se o método da requisição for do tipo POST, cria um novo post.
    if request.method == "POST":
        # Instância a classe que representa o formulário de criação
        # de um post novo para receber os dados enviados na requisição.
        form = PostForm(request.POST)
        # Realiza todas as validações dos campos e dos tipos de dados
        # inseridos, com base no que foi definido no model Post. Caso todos
        # os campos forem validados, `is_valid` retorna True.
        if form.is_valid():
            # cria um novo objeto para ser armazenado no banco de dados a
            # partir dos dados do formulário. `commit=False` indica que
            # esse registro não deve ser salvo no banco de dados ainda.
            new_post = form.save(commit=False)
            # Cria o slug do post a partir do título dele.
            new_post.slug = slugify(new_post.title)
            # Salva de fato o post no banco de dados.
            new_post.save()
            # Redireciona para a view `index`.
            return HttpResponseRedirect(reverse("index"))
    else:
        # Caso não for o método POST, retorna o formulário vazio.
        form = PostForm()

    # Renderiza o template HTML do formulário, passando a requisição, o
    # nome do template e os dados no contexto, no caso passa o `form` para
    # renderizar os campos de input.
    return render(request, "new_post.html", {"form": form})


# Class view, cria uma view usando classe para representar a view, ela
# herda de `ListView` todo o código boilerplate para listar os posts, simplificando
# o processo e reduzindo código.
class PostList(ListView):
    # Define que essa view está atrelada ao model `Post`.
    model = Post
    # Indica qual o template que ela vai usar para exibir as informações.
    template_name = "index.html"
    # Realiza a query no banco de dados retornando todos os posts que
    # possui `published=True` (que estão publicados).
    queryset = Post.objects.filter(published=True)


# Class view, representa a view para exibir os dados de um único post.
# Herda de `DetailView` as funcionalidades necessárias para isso, código boilerplate.
class PostDetail(DetailView):
    # Indica que a view está atrelada ao model Post.
    model = Post
    # Define explicitamente qual o nome do template usado para essa view.
    template_name = "detail.html"
