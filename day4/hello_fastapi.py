# Classe para instanciar o entrypoint principal do FastAPI.
from fastapi import FastAPI

# Classe para criar enums em Python.
from enum import Enum

# Instanciando o entrypoint principal da aplicação.
app = FastAPI()


# Enum para mostrar opções de uma lista para um parâmetro. São compostos
# por uma chave e um valor.
class ListOption(str, Enum):
    USER = "user"
    DEPARTMENT = "department"
    ACCOUNT = "account"


# Todas as rotas definidas no FastAPI são assíncronas, ou seja, são corrotinas
# e possuem todo o poder da programação assíncrona, mesmo que elas sejam
# declaradas sem o `async`, por baixo dos panos o FastAPI ainda sim vai transformá-las
# em corrotinas.


# Criando uma rota GET. Onde `list_option` é um parâmetro dinâmico que pode
# ser inserido na rota.
# Esse parâmetro utiliza o Enum `ListOption` para delimitar as opções que
# podem ser utilizadas no parâmetro `list_option`, como uma espécie de
# validação. Caso for inserido um valor diferente, retorna um erro.
@app.get("/{list_option}/list")
async def generic_list(list_option: ListOption):
    # Comparando qual opção foi inserida e definindo quais dados vão retornar.
    if list_option == ListOption.USER:
        data = ["jim", "pam", "dwight"]
    elif list_option == ListOption.DEPARTMENT:
        data = ["Sales", "Management", "IT"]
    elif list_option == ListOption.ACCOUNT:
        data = [123, 456, 789]

    # Retorna um dicionário como Response. Por padrão, o FastAPI já realiza
    # a serialização para JSON automaticamente.
    return {list_option: data}


# Outra rota do tipo GET com um parâmetro de rota `username`. Dessa vez,
# o parâmetro tem a validação do tipo string, se outro tipo for inserido,
# vai retornar erro.
@app.get("/user/{username}")
async def user_profile(username: str):
    # Retorna um dicionário para ser serializado para JSON.
    return {"data": username}


# Outra rota do tipo GET com o parâmetro `number`, possui validação do
# tipo inteiro e também retorna um JSON serializado, por padrão.
@app.get("/account/{number}")
async def account_detail(number: int):
    return {"account": number}


# Outra rota do tipo GET com um parâmetro chamado `filepath` do tipo string,
# porém, este parâmetro por ser um caminho para um arquivo, ele necessita de
# validação especial, por isso adiciona-se `:path` na frente dele na rota,
# dessa forma, o FastAPI entende que mesmo que tenha diversas barras (/) após
# `/import/` elas indicam um caminho de um arquivo e não rotas diferentes.
@app.get("/import/{filepath:path}")
async def import_file(filepath: str):
    # Retorna, a partir de um dicionário, um JSON serializado.
    return {"importing": filepath}
