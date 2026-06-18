#Classe que recebe duas cidades e retorna o custo para colocar na aresta
import requests
from dotenv import load_dotenv
import os

class City:
    def __init__(self, name):
        self.name = name
        self.coordenada = {
            "latitude": None,
            "longitude": None
        }
        self.altitude = None

class Custo:
    def __init__(self, A, B):
        load_dotenv()
        self._api_key = os.getenv("API_KEY")
        self.A = City(A) #cidade A
        self.B = City(B) #cidade B

        #Coloca as coordenadas
        self._coordenadas()

    # Retorna a distância entre dois pontos
    def _distancia(self):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes" # API google
        mask = "routes.distanceMeters"#dados que quero da requisição
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": mask
        }
        #Json das cidades
        json = {
            "origin": {"address": self.A.name},
            "destination": {"address": self.B.name},
            "travelMode": "DRIVE"
        }
        try:
            response = requests.post(url, headers=headers, json=json)
            # Coleta o resposta
            if response.status_code == 200:
                if response.json() != {}:
                    distancia = response.json()["routes"][0]["distanceMeters"]
                else:
                    # CASO FALHE A REQUISIÇÃO PELO NOME DAS CIDADES
                    # TENTA FAZER A REQUISIÇÃO PELAS COORDENADAS DA CIDADE
                    json_coordenadas = {
                        "origin": {
                            "location": {
                                "latLng": {
                                    "latitude": self.A.coordenada["latitude"],
                                    "longitude": self.A.coordenada["longitude"]
                                }
                            }
                        },
                        "destination": {
                            "location": {
                                "latLng": {
                                    "latitude": self.B.coordenada["latitude"],
                                    "longitude": self.B.coordenada["longitude"]
                                }
                            }
                        },
                        "travelMode": "DRIVE"
                    }
                    response2 = requests.post(url, headers=headers, json=json_coordenadas)

                    if response2.status_code == 200 and "routes" in response2.json() and len(
                            response2.json()["routes"]) > 0:
                        distancia = response2.json()["routes"][0]["distanceMeters"]
                    else:
                        print(
                            f"Erro Crítico: Google não encontrou nenhuma rota viável de carro. Resposta: {response2.text}")
        except Exception as e:
            print(f"ERRO ao tentar achar distancia entre {self.A.name} e {self.B.name}: ", e)

        return float(distancia)
    # Insere a altitude duas cidades e retorna a diferença de altura entre as cidades
    def _altitude(self):
        for city in (self.A, self.B):
            #caso já tenha calculado altitudo não recalcula
            if (city.altitude is not None):
                continue

            url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={city.coordenada["latitude"]}%2C{city.coordenada["longitude"]}&key={self._api_key}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    city.altitude = response.json()["results"][0]["elevation"]
            except Exception as e:
                print(f"Erro ao calcular altitude da cidade {city.name}: ", e)

        #Retorna a diferença de altitude do ponto A ao B
        return float(self.A.altitude) - float(self.B.altitude)
    # Insere coordenada nas cidades
    def _coordenadas(self):
        for city in self.A, self.B:
            try:
                url = f"https://geocode.googleapis.com/v4/geocode/address/{city.name.replace(" ", "+")}?key={self._api_key}" #API para coordenada
                response = requests.get(url)
                response.raise_for_status() #caso tenha falhado a requisição mostra erro
                if response.status_code == 200:
                    city.coordenada["longitude"] = response.json()["results"][0]["location"]["longitude"]
                    city.coordenada["latitude"] = response.json()["results"][0]["location"]["latitude"]
            except Exception as e:
                print(f"Erro ao coletar coordenada da cidade : {city.name}: ", e)

# Retorna o peso da aresta
def peso(A, B):
    # Caso seja o trecho que use balsa
    if "Porto Murtinho, Brasil" in (A, B) or "Carmelo Peralta, Paraguai" in (A, B):
        weight = (1 * 500)+(10*60) #1m/s * 500m + espera de 10min
    else: # Se não o calculo de peso é normal
        c = Custo(A, B)
        # Se for descida o veiculo percorre a uma velocidade de 100km/h (28m/s) do contrario 80km/h (22m/s)
        velocidade = 22 if c._altitude() < 0 else 28
        weight = velocidade*c._distancia()

    return weight