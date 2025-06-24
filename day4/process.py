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
    
    
    # Cria um gerenciador de contexto que vai ter disponível a execução usando processos e paralelismo,
    # neste caso, cada processo vai ser aberto em um novo núcleo, tendo sua execução isolada e independente.
    # É uma abstração em cima de multi_processing.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Cria um processo para a função de `consulta_dados` e como ela pode retornar algo, espera-se
        # uma promise, que em algum momento vai retornar.
        future = executor.submit(consulta_dados)

        # Obriga o executor a esperar a promise anterior de fato ser concluída, pois os dados serão
        # necessários para a próxima execução.
        dados = future.result()

        # Cria outro processo para executar `processa_dados` que vai utilizar os dados da promise,
        # ao fazer isso, cria-se uma dependência interna, onde a função `processa_dados` só vai ser
        # executada após a promise da `consulta_dados` terminar.
        executor.submit(processa_dados, dados)

        # Cria vários processos para a função `grava_log` para realizar seu processamento em paralelo.
        # Por ela ser independente, é possível executá-la sozinha em paralelo com as outras.
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)

    print("Fim")
    # Contador para pegar o tempo percorrido até agora.
    finish = time.perf_counter()
    # Imprimindo o tempo que levou para executar todo o trecho, fazendo a diferença entre
    # o início do contador e o contador final.
    print(f"Finished in: {round(finish - start, 2)} seconds")


# É necessário usar esse controle ao trabalhar com processos e paralelismo.
if __name__ == "__main__":
    main()
