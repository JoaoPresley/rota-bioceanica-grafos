import time
import networkx as nx
import os
from Grafo import AnalisadorRota

def main():
    analisador = AnalisadorRota()
    
    recalcular = False
    if os.path.exists(analisador.cache_file):
        escolha = input(f"Arquivo de cache '{analisador.cache_file}' encontrado. Deseja recalcular os pesos? (s/N): ").lower()
        if escolha == 's':
            recalcular = True
    
    G = analisador.construir_grafo(recalcular=recalcular)

    # --- CONFIGURAÇÃO DA ANÁLISE DO GRUPO ---
    CIDADE_ORIGEM = "Santos, São Paulo, Brasil"
    CIDADE_DESTINO = "Iquique, Tarapacá, Chile"

    print("-" * 70)
    print(f"Análise de Rota Bioceânica: {CIDADE_ORIGEM} ➔ {CIDADE_DESTINO}")
    print("-" * 70)

    # --- 1. ALGORITMO DE DIJKSTRA ---
    inicio_dijkstra = time.perf_counter()
    try:
        caminho_dijkstra = nx.dijkstra_path(G, source=CIDADE_ORIGEM, target=CIDADE_DESTINO, weight="weight")
        custo_dijkstra = nx.dijkstra_path_length(G, source=CIDADE_ORIGEM, target=CIDADE_DESTINO, weight="weight")
    except nx.NetworkXNoPath:
        print("Erro: Não foi encontrado um caminho usando Dijkstra.")
        return

    fim_dijkstra = time.perf_counter()
    tempo_exec_dijkstra = fim_dijkstra - inicio_dijkstra

    # --- 2. ALGORITMO DE FLOYD-WARSHALL ---
    inicio_floyd = time.perf_counter()
    predecessores, distancias = nx.floyd_warshall_predecessor_and_distance(G, weight="weight")
    
    if CIDADE_DESTINO not in distancias[CIDADE_ORIGEM]:
        print("Erro: Não foi encontrado um caminho usando Floyd-Warshall.")
        return
        
    caminho_floyd = nx.reconstruct_path(CIDADE_ORIGEM, CIDADE_DESTINO, predecessores)
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
        print("   Ambos os algoritmos encontraram exatamente o MESMO caminho e o mesmo custo ideal.")
        print("   Isso valida a exatidão matemática de ambos para encontrar o ótimo global.")
    else:
        print(f"   Divergência detectada! Caminhos físicos diferentes, mas custos idênticos ({custo_dijkstra:.2f}).")
        print("   Isso prova a existência de caminhos alternativos/empates técnicos na malha rodoviária.")

if __name__ == "__main__":
    main()
