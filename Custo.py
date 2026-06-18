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
        response = requests.post(url, headers=headers, json=json)
        # Coleta o resposta
        if response.status_code == 200:
            distancia = response.json()["routes"][0]["distanceMeters"]

        return distancia
    # Retorna a diferença de altura entre as duas cidades
    def _altitude(self):
        altitude = self.A + self.B
        return altitude
    def _coordenadas(self):
        coordenadas = self.A + self.B
        return coordenadas
    # Retorna o peso da aresta

def peso(A, B):
    c = Custo(A, B)
    peso = 3.6 * 500
    return peso