#Grafo que funcionará para criar a analise da melhor rota bioceânica
import time
import networkx as nx
import numpy as np
from dotenv import __main__

from Custo import peso

import dask
from dask.distributed import Client
def paralel(conections):
    client = Client()

    print(f"Iniciada paralelização para calculo de custo entre cidades\n"
          f"-----Painel de controle rodando em: {client.dashboard_link} --------")
    # 1. Cria função dask para rodar em paralelo
    func_paralela = dask.delayed(peso)

    # 2. Cria variavel que quarda as tarefas "atrasadas" delayed
    tarefas = []

    # 3. Preenche as tarefas com o funcao que sera executada
    for origem, destino in conections:
        peso_futuro = func_paralela(origem, destino)#Calcula o peso entre as cidades
        tarefas.append((origem, destino, peso_futuro))

    # 4. Executa o parelelismo
    print("-----Iniciado calculo paralelo---------")
    resultados = dask.compute(*tarefas)
    return resultados

def main():
    # Abre o arquivo de rotas e o lê as conexões entre as cidades
    with open(r"rotas.txt", 'r', encoding="utf-8-sig") as f:
        #
        #   Me entrega a variavel ** conections **
        #       -> Formato [ [cidade A, Cidade B] , [Cidade B, Cidade C] ...]
        #       -> Sendo que as duplas dentro da lista formam conexões entre si
        #
        conections = f.readlines()
        conections = [x.strip() for x in conections]
        conections = [x.split(" <-> ") for x in conections]

    # Obtem a lista de cidades que estão nas conecxões
    cities = np.unique(np.array(conections).flatten())

    # Cria um grafo com as cidades
    G = nx.Graph()
    G.add_nodes_from(cities)

    # Paralelismo para obter os pesos entre as cidades
    pesos = paralel(conections)

    #   Adiciona as arestas com o peso
    for origem, destino, w in pesos:
        print(f"Adicionando peso de {origem} para {destino}...")
        G.add_edge(origem, destino, weight=w)

    # --- CONFIGURAÇÃO DA ANÁLISE DO GRUPO ---
    CIDADE_ORIGEM = "Santos"
    CIDADE_DESTINO = "Iquique"

    print("-" * 70)
    print(
        f"Análise de Rota Bioceânica: {CIDADE_ORIGEM} ➔ {CIDADE_DESTINO}"
    )
    print("-" * 70)

    # --- 1. ALGORITMO DE DIJKSTRA ---
    inicio_dijkstra = time.perf_counter()

    caminho_dijkstra = nx.dijkstra_path(
        G, source=CIDADE_ORIGEM, target=CIDADE_DESTINO, weight="weight"
    )
    custo_dijkstra = nx.dijkstra_path_length(
        G, source=CIDADE_ORIGEM, target=CIDADE_DESTINO, weight="weight"
    )

    fim_dijkstra = time.perf_counter()
    tempo_exec_dijkstra = fim_dijkstra - inicio_dijkstra


    # --- 2. ALGORITMO DE FLOYD-WARSHALL ---
    inicio_floyd = time.perf_counter()

    predecessores, distancias = nx.floyd_warshall_predecessor_and_distance(
        G, weight="weight"
    )
    caminho_floyd = nx.reconstruct_path(
        CIDADE_ORIGEM, CIDADE_DESTINO, predecessores
    )
    custo_floyd = distancias[CIDADE_ORIGEM][CIDADE_DESTINO]

    fim_floyd = time.perf_counter()
    tempo_exec_floyd = fim_floyd - inicio_floyd


    # --- 3. APRESENTAÇÃO DOS RESULTADOS ---
    print(f"\n▶ RESULTADOS - ALGORITMO DE DIJKSTRA:")
    print(f"   * Melhor Caminho: {' ➔ '.join(caminho_dijkstra)}")
    print(f"   * Custo Total Obtido: {custo_dijkstra:.2f}")
    print(f"   * Tempo de Execução Real: {tempo_exec_dijkstra:.6f} segundos")
    print(f"   * Complexidade Teórica (Big O): O(E + V log V)")

    print(f"\n▶ RESULTADOS - ALGORITMO DE FLOYD-WARSHALL:")
    print(f"   * Melhor Caminho: {' ➔ '.join(caminho_floyd)}")
    print(f"   * Custo Total Obtido: {custo_floyd:.2f}")
    print(f"   * Tempo de Execução Real: {tempo_exec_floyd:.6f} segundos")
    print(f"   * Complexidade Teórica (Big O): O(V³)")

    print("-" * 70)

    # --- 4. OBSERVAÇÕES SOBRE AS SOLUÇÕES ---
    print("\n▶ OBSERVAÇÕES SOBRE IGUALDADE OU DIFERENÇA:")
    if caminho_dijkstra == caminho_floyd:
        print(
            "   Ambos os algoritmos encontraram exatamente o MESMO caminho e o mesmo custo ideal."
        )
        print(
            "   Isso valida a exatidão matemática de ambos para encontrar o ótimo global."
        )
    else:
        print(
            f"   Divergência detectada! Caminhos físicos diferentes, mas custos idênticos ({custo_dijkstra:.2f})."
        )
        print(
            "   Isso prova a existência de caminhos alternativos/empates técnicos na malha rodoviária."
        )

if __name__ == "__main__":
    main()
