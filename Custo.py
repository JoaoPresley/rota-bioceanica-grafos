#Classe que recebe duas cidades e retorna o custo para colocar na aresta
import requests
from dotenv import load_dotenv
import os

class City:
    def __init__(self, name):
        self.name = name
        self.coordenada = {
            "latitude": "",
            "longitude": ""
        }
        self.altitude = None

class Custo:
    def __init__(self, A, B):
        self._api_key = os.getenv("API_KEY")
        self.A = City(A) #cidade A
        self.B = City(B) #cidade B
    # Retorna a distância entre dois pontos
    def _distancia(self):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes" # API google
        mask = "routes.distanceMeters"#dados que quero da requisição
        headers = {
            "Content-Type: application/json",
            f"X - Goog - Api - Key: {self._api_key}",
            f"X-Goog-FieldMask: {mask}"

        }
        #Json das cidades
        json = {
            "origin": {"address": self.A},
            "destination": {"address": self.B},
            "travelMode": "DRIVE"
        }
        try:
            response = requests.post(url, headers=headers, json=json)
            # Coleta o resposta
            if response.status_code == 200:
                distancia = response.json()["routes"][0]["distanceMeters"]
        except Exception as e:
            print(f"ERRO ao tentar achar distancia entre {self.A.name} e {self.B.name}: ", e)

        return distancia
    # Insere a altitude duas cidades
    def _altitude(self):
        for city in (self.A, self.B):
            url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={city.coordenada["latitude"]}%2C{city.coordenada["longitude"]}&key={self._api_key}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    city.altitude = response.json()["results"][0]["elevation"]
            except Exception as e:
                print(f"Erro ao calcular altitude da cidade {city.name}: ", e)
    # Insere coordenada nas cidades
    def _coordenadas(self):
        for city in self.A, self.B:
            try:
                url = f"https://geocode.googleapis.com/v4/geocode/address/{self.A.name.replace(" ", "+")}?key={self._api_key}" #API para coordenada
                response = requests.get(url)
                if response.status_code == 200:
                    city.coordenada["longitude"] = response.json()["results"][0]["location"]["longitude"]
                    city.coordenada["latitude"] = response.json()["results"][0]["location"]["latitude"]
            except Exception as e:
                print(f"Erro ao coletar coordenada da cidade : {city.name}: ", e)

# Retorna o peso da aresta
def peso(A, B):
    c = Custo(A, B)
    peso = 3.6 * 500
    return peso