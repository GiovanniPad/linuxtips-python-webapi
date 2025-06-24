# Biblioteca para manipular valores de tempo.
import time

# Biblioteca para programação assíncrona com foco em operações de IO Bound.
import asyncio

# Todas funções que tem `async` vão retornar promises ou futures, que é uma
# promessa que em algum momento vai retornar um valor (ao terminar sua execução).
# Ao usar `async` na função ela passa a ser uma corrotina.

# O uso da palavra `await` faz com que a execução seja pausada para aguardar até
# que a promise/future termine sua execução.

# Ao usar `async` a função passa a ser uma corrotina, uma corrotina
# é uma espécie de função com suporte a operações assíncronas.
async def consulta_dados():
    print("Consultando dados...")
    # Simula um tempo de espera de 2 segundos de forma assíncrona.
    # Usar `await` informa ao interpretador que aqui é necessário esperar
    # a execução terminar.
    await asyncio.sleep(2)
    return "dados"


# Outra corrotina criada com `async` com suporte a operações assíncronas.
async def processa_dados(dados):
    print("Processando dados...")
    print(dados)
    # Pausa a execução com o `await` e espera a execução do `sleep` terminar.
    await asyncio.sleep(2)


# Corrotina criada com `async` com suporte a operações assíncronas.
async def grava_log():
    print("Gravando log...")
    # Pausa a execução com o `await` e espera a execução do `sleep` terminar.
    await asyncio.sleep(2)


# Corrotina principal.
async def main():  
    # Para executar uma corrotina de forma assíncrona e não bloqueante
    # é necessário tranformá-la em uma task mandando a corrotina para o event loop.
    
    # Nesta situação a palavra await tem um papel muito importante, pois ao usá-la
    # dentro de uma task async, a execução da corrotina vai ser suspensa e no lugar
    # dela vai ser executados outras corrotinas que estão na fila, dessa forma
    # o código fica não bloqueante, enquanto espera a operação de um terminar, outro
    # é executado.
    
    # Porém, neste caso, não temos mais controle na ordem de execução das funções, pois
    # elas vão ser executadas conforme for possível, sendo gerenciadas automaticamente
    # pelo sistema operacional.

    # Cria uma task a partir de uma corrotina e como é uma função de consulta de dados
    # atribui a variável `dados` que vira uma promise, que em algum momento vai retornar
    # algo.
    # O uso do `await` neste caso é necessário pois esses dados vão ser essenciais para que
    # a execução da próxima função funcione, então é necessário aguardar sua execução.
    dados = await asyncio.create_task(consulta_dados())

    # Cria uma outra task que recebe os dados (aqui a promise já terminou por conta do await anterior).
    # Essa aqui só vai ser executada após a task anterior for terminada, por conta do await cria-se
    # uma relação de dependência entre as duas.
    asyncio.create_task(processa_dados(dados))

    # Outra task criada, porém essa não possui dependência nenhum, dessa forma ela vai ser executada em
    # paralelo com as outras tasks. Em outro processo.
    asyncio.create_task(grava_log())


if __name__ == "__main__":
    # Performa um contador para ver o tempo demorado para executar um trecho de
    # instruções
    start = time.perf_counter()
    print("Início")

    # Aqui se inicia o event loop, é o principal que faz tudo funcionar, o loop que fica coletando
    # as tarefas pendentes e gerenciando toda a execução de promises.
    asyncio.run(main())

    print("Fim")
    # Contador para pegar o tempo percorrido até agora.
    finish = time.perf_counter()
    # Imprimindo o tempo que levou para executar todo o trecho, fazendo a diferença entre
    # o início do contador e o contador final.
    print(f"Finished in: {round(finish - start, 2)} seconds")
