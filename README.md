# 🗺️ Análise da Rota Bioceânica com Grafos

Este projeto utiliza a **Teoria dos Grafos** para analisar e determinar a melhor rota bioceânica entre cidades da América do Sul. O sistema modela as conexões rodoviárias reais e calcula o custo de cada trecho de forma inteligente, comparando a eficiência de diferentes algoritmos de busca de caminho.

O diferencial do projeto é a precisão do cálculo de custo, que vai além da distância kilométrica, integrando fatores como **relevo (altimetria)** e **travessias de balsa**.

---

## 🚀 Funcionalidades

* **Representação em Grafos**: Cidades funcionam como nós (vértices) e as rodovias como arestas em um grafo não direcionado.
* **Cálculo Dinâmico de Custo**: O peso de cada aresta baseia-se no tempo de viagem, influenciado por:
    * *Plano/Descida*: Velocidade média de 100 km/h (~28 m/s).
    * *Subida*: Velocidade reduzida para 80 km/h (~22 m/s) devido à inclinação.
    * *Balsa*: Velocidade de 3.6 km/h (~1 m/s) somada a um tempo fixo de espera.
* **Algoritmos de Roteamento**: Implementação e comparação de performance entre **Dijkstra** e **Floyd-Warshall**.
* **Processamento Paralelo**: Uso da biblioteca `dask` para paralelizar o cálculo de custo das arestas, ideal para escalabilidade do grafo.
* **Integração com Google Maps API**: Consumo em tempo real de altimetria, distâncias e coordenadas geográficas.

---

## 🛠️ Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
* [Python 3.8+](https://www.python.org/)
* [Pip](https://pip.pypa.io/en/stable/) (Gerenciador de pacotes do Python)

### 🔑 Chave de API do Google Cloud
O projeto exige uma chave de API ativa com os seguintes serviços habilitados:
1.  **Google Maps Directions API**
2.  **Google Maps Elevation API**
3.  **Google Maps Geocoding API**

> 💡 **Como obter a chave:** Acesse o [Google Cloud Console](https://console.cloud.google.com/), crie um projeto, ative as APIs mencionadas acima e gere sua credencial (Chave de API).

---

## ⚙️ Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone [https://github.com/JoaoPresley/rota-bioceanica-grafos.git](https://github.com/JoaoPresley/rota-bioceanica-grafos.git)
cd rota-bioceanica-grafos
```
### 2. Instalar DependênciasInstale todos os pacotes necessários rodando:
```Bash
pip install -r requirements.txt
```
Caso o arquivo não esteja presente, instale manualmente:
```Bash
pip install networkx numpy python-dotenv requests dask dask-distributed
```
### 3. Configurar as Variáveis de Ambiente
Na raiz do projeto, você encontrará um arquivo chamado ```.env_example```.
1. Duplique ou renomeie este arquivo para ```.env```:
   ```Bash
   cp .env_example .env
   ```
2. Abra o arquivo .env e insira sua chave do Google Cloud:
   ```Snippet de código
   API_KEY=SUA_CHAVE_DE_API_AQUI
   ```
⚠️ Aviso de Segurança: Nunca envie seu arquivo .env para repositórios públicos. Ele já está configurado no .gitignore.
## 🏃 Como Rodar o Projeto
Com tudo configurado, execute o script principal:
   ```Bash
   python Grafo.py
   ```
O que o script faz?
1. Carrega a malha rodoviária definida em rotas.txt.
2. Consulta as APIs do Google para calcular os pesos exatos das conexões (distância + altitude).
3. Calcula a melhor rota entre a origem (Santos, SP, Brasil) e o destino (Iquique, Tarapacá, Chile).
4. Exibe no terminal o trajeto ideal, custo total estimado, tempo de execução e a comparação de complexidade entre os algoritmos.
## 📁 Estrutura do Projeto

| Arquivo / Pasta | Descrição |
| :--- | :--- |
| `Grafo.py` | Script principal. Monta o grafo, gere o processamento paralelo com `dask` e executa as buscas. |
| `Custo.py` | Regras de negócio e física do projeto. Faz o cálculo de tempo/gasto integrando as APIs do Google. |
| `rotas.txt` | Banco de dados simplificado mapeando as conexões no formato `Cidade A <-> Cidade B`. |
| `.env_example` | Modelo para configuração das credenciais locais. |

---

## 🤝 Contribuição

A sua ajuda é muito bem-vinda! Sinta-se à vontade para:
* Abrir uma **Issue** para relatar bugs ou sugerir melhorias.
* Enviar um **Pull Request** com otimizações de código ou novas rotas.

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
