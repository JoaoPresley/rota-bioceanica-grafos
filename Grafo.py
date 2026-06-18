# Grafo que funcionará para criar a analise da melhor rota bioceânica
import networkx as nx
import numpy as np
import dask
from dask.distributed import Client
from Custo import peso
import os
import json

class AnalisadorRota:
    def __init__(self, rotas_file="rotas.txt", cache_file="grafo_cache.json"):
        self.rotas_file = rotas_file
        self.cache_file = cache_file
        self.G = nx.Graph()

    def carregar_conexoes(self):
        with open(self.rotas_file, 'r', encoding="utf-8-sig") as f:
            conections = f.readlines()
            conections = [x.strip() for x in conections]
            conections = [x.split(" <-> ") for x in conections]
        return conections

    def paralel(self, conections):
        client = Client()
        print(f"Iniciada paralelização para calculo de custo entre cidades\n"
              f"-----Painel de controle rodando em: {client.dashboard_link} --------")
        
        func_paralela = dask.delayed(peso)
        tarefas = []

        for origem, destino in conections:
            peso_futuro = func_paralela(origem, destino)
            tarefas.append((origem, destino, peso_futuro))

        print("-----Iniciado calculo paralelo---------")
        resultados = dask.compute(*tarefas)
        client.close()
        return resultados

    def salvar_grafo(self):
        # Salva as arestas e pesos em um arquivo JSON para persistência
        dados_grafo = []
        for u, v, data in self.G.edges(data=True):
            dados_grafo.append({
                "origem": u,
                "destino": v,
                "weight": data["weight"]
            })
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(dados_grafo, f, ensure_ascii=False, indent=4)
        print(f"Grafo salvo em {self.cache_file}")

    def carregar_grafo_cache(self):
        if not os.path.exists(self.cache_file):
            return False
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                dados_grafo = json.load(f)
            
            self.G.clear()
            for edge in dados_grafo:
                self.G.add_edge(edge["origem"], edge["destino"], weight=edge["weight"])
            return True
        except Exception as e:
            print(f"Erro ao carregar cache: {e}")
            return False

    def construir_grafo(self, recalcular=False):
        conections = self.carregar_conexoes()
        
        if not recalcular and self.carregar_grafo_cache():
            print("Utilizando pesos carregados do cache.")
            return self.G

        print("Calculando novos pesos...")
        cities = np.unique(np.array(conections).flatten())
        self.G.clear()
        self.G.add_nodes_from(cities)

        pesos = self.paralel(conections)

        for origem, destino, w in pesos:
            self.G.add_edge(origem, destino, weight=w)
        
        self.salvar_grafo()
        return self.G
