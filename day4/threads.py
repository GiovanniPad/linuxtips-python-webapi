# Biblioteca para manipular valores de tempo.
import time
# Módulo para executar tarefas assíncronas utilizando concorrência com threads
# ou processos.
import concurrent.futures


# Função para consultar dados de algo externo, por conta disso ela é uma
# função I/O Bound.
def consulta_dados():
    print("Consultando dados...")
    # Simula um tempo de espera de 2 segundos.
    time.sleep(2)
    return "dados"


# Função para realizar o processamento de determinado conjunto de dados,
# ela depende mais do processador, por isso é CPU Bound.
def processa_dados(dados):
    print("Processando dados...")
    # Simula um tempo de espera de 2 segundos.
    time.sleep(2)


# Função para gravar logs em algum lugar, normalmente em arquivos, por conta
# disso ela também é de I/O Bound, por precisa escrever.
def grava_log():
    print("Gravando log...")
    # Simula um tempo de espera de 2 segundos.
    time.sleep(2)


# Função principal do programa.
def main():
    # Performa um contador para ver o tempo demorado para executar um trecho de
    # instruções
    start = time.perf_counter()
    print("Início")
    
    # Abre um gerenciador de contexto e nele vai ter um executor que vai abrir
    # uma ThreadPool para executar todo o código dentro desse contexto de maneira
    # concorrente utilizando threads.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Adiciona a função `consulta_dados` a pool de funções e como ela retorna um
        # valor, é definido um `future`, que é uma espécie de promessa que em algum
        # momento ela vai retornar algo. A partir daqui é criada uma thread exclusiva.
        future = executor.submit(consulta_dados)
        # Cria uma dependência entre a variável dados e o resultado da função `consulta_dados`,
        # pois a variável `dados` só vai existir quando a função `consulta_dados` retornar seu
        # valor através da `future`, `result()` serve para retornar esse valor.
        dados = future.result()
        # Adiciona a função `processa_dados` a pool das threads, incluindo a variável `dados`
        # como parâmetro e por conta dessa variável depender da `future` da função `consulta_dados`,
        # logo, ela depende do retorno da função `consulta_dados` para funcionar, assim, a função
        # `processa_dados` só vai executar após a função `consulta_dados` retornar seu valor a `future`.
        # A thread criada exclusiva criada anteriormente vai até aqui como uma única thread.
        executor.submit(processa_dados, dados)

        # Adiciona a função `grava_log` a fila/pool de funções para as threads executarem. Como essa
        # função não depende de nenhuma outra função para executar, ela vai poder ser executada de forma
        # concorrente com a função `consulta_dados`, porém para ela vai ser aberta um novo canal de
        # comunicação, ou seja, outra thread.
        # Dessa forma, será possivelmente executar essa função sem esperar que a `consulta_dados` e a
        # `processo_dados` acabe, fazendo com que o tempo de execução diminua.
        executor.submit(grava_log)

    print("Fim")
    # Contador para pegar o tempo percorrido até agora.
    finish = time.perf_counter()
    # Imprimindo o tempo que levou para executar todo o trecho, fazendo a diferença entre
    # o início do contador e o contador final.
    print(f"Finished in: {round(finish - start, 2)} seconds")

main()