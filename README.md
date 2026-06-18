# Análise da Rota Bioceânica com Grafos

Este projeto tem como objetivo analisar e encontrar a melhor rota bioceânica entre cidades da América do Sul, utilizando a teoria dos grafos e comparando a eficiência de diferentes algoritmos de busca de caminho. O foco principal é modelar as conexões rodoviárias e calcular o custo de cada trecho, considerando fatores como distância, relevo e travessias de balsa.

## Funcionalidades

*   **Modelagem de Grafos**: Representação de cidades como nós e conexões rodoviárias como arestas em um grafo não direcionado.
*   **Cálculo de Custo de Arestas**: Determinação do peso de cada aresta com base na distância, diferença de altitude (influenciando a velocidade em subidas e descidas) e travessias de balsa.
    *   **Velocidades Consideradas**:
        *   **Descida/Plano**: 100 km/h (aproximadamente 28 m/s)
        *   **Subida**: 80 km/h (aproximadamente 22 m/s)
        *   **Balsa**: 3.6 km/h (aproximadamente 1 m/s), com um custo adicional de tempo de espera.
*   **Algoritmos de Busca de Caminho**: Implementação e comparação dos algoritmos de Dijkstra e Floyd-Warshall para encontrar o caminho de menor custo entre uma cidade de origem e uma de destino.
*   **Paralelização**: Utilização da biblioteca `dask` para paralelizar o cálculo dos custos das arestas, otimizando o desempenho para grafos maiores.
*   **Integração com APIs do Google**: Utilização das APIs de Directions, Elevation e Geocoding do Google para obter dados de distância, altitude e coordenadas geográficas das cidades.

## Pré-requisitos

Para rodar este projeto, você precisará ter instalado:

*   **Python 3.x**
*   **pip** (gerenciador de pacotes Python)
*   **Chave de API do Google Cloud**: Uma chave de API válida com acesso às seguintes APIs:
    *   Google Maps Directions API
    *   Google Maps Elevation API
    *   Google Maps Geocoding API

## Instalação

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local:

1.  **Clone o repositório**:

    ```bash
    git clone https://github.com/JoaoPresley/rota-bioceanica-grafos.git
    cd rota-bioceanica-grafos
    ```

2.  **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

    (Se o arquivo `requirements.txt` não existir, você pode criá-lo com as seguintes dependências e depois instalá-las):

    ```bash
    pip install networkx numpy python-dotenv requests dask dask-distributed
    ```

## Configuração da Chave de API

Este projeto utiliza variáveis de ambiente para gerenciar a chave de API do Google Cloud. Siga as instruções:

1.  **Crie um arquivo `.env`**: Na raiz do projeto, crie um arquivo chamado `.env`.

2.  **Adicione sua chave de API**: Abra o arquivo `.env` e adicione sua chave de API do Google Cloud no formato `API_KEY=SUA_CHAVE_DE_API_AQUI`. Você pode usar o arquivo `.env_example` como referência.

    Exemplo de `.env_example`:

    ```
    API_KEY=SUA_CHAVE_DE_API_AQUI
    ```

    **Importante**: Substitua `SUA_CHAVE_DE_API_AQUI` pela sua chave de API real do Google Cloud. Mantenha seu arquivo `.env` privado e nunca o comite em repositórios públicos.

## Como Rodar o Projeto

Após a instalação e configuração da chave de API, você pode executar o script principal:

```bash
python main.py
```

O sistema agora conta com um mecanismo de persistência. Na primeira execução, os pesos das arestas serão calculados e salvos em `grafo_cache.json`. Nas execuções seguintes, o script perguntará se você deseja utilizar os dados salvos ou recalcular tudo.

O script `main.py` irá:

1.  Ler as conexões de cidades do arquivo `rotas.txt`.
2.  Calcular os pesos das arestas utilizando as APIs do Google e a lógica de custo definida em `Custo.py`.
3.  Executar os algoritmos de Dijkstra e Floyd-Warshall para encontrar o melhor caminho entre as cidades de origem e destino (atualmente configuradas como "Santos, São Paulo, Brasil" e "Iquique, Tarapacá, Chile").
4.  Imprimir os resultados, incluindo o caminho encontrado, o custo total, o tempo de execução e a complexidade teórica de cada algoritmo.

## Estrutura do Projeto

*   `main.py`: Ponto de entrada do programa. Gerencia a interface com o usuário e a execução dos algoritmos de busca.
*   `Grafo.py`: Contém a classe `AnalisadorRota`, responsável pela construção do grafo, integração com DASK para processamento paralelo e persistência dos dados (cache).
*   `Custo.py`: Define a classe `Custo` e a função `peso` para calcular o custo entre duas cidades. Integra-se com as APIs do Google para obter distâncias, altitudes e coordenadas geográficas.
*   `rotas.txt`: Um arquivo de texto que lista as conexões rodoviárias entre as cidades, no formato `Cidade A <-> Cidade B`.
*   `.env_example`: Um arquivo de exemplo para a configuração da chave de API do Google Cloud.
*   `README.md`: Este documento, fornecendo uma visão geral do projeto, instruções de instalação, configuração e uso.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou Pull Requests para melhorias, correções de bugs ou novas funcionalidades.

## Licença

[Adicionar informações de licença aqui, se aplicável]
