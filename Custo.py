#Classe que recebe duas cidades e retorna o custo para colocar na aresta
class custo:
    def __init__(self, A, B):
        self.A = A #cidade A
        self.B = B #cidade B
    # Retorna a distância entre dois pontos
    def _distancia(self):
        distancia = self.A + self.B
        return distancia
    # Retorna a diferença de altura entre as duas cidades
    def _altitude(self):
        altitude = self.A + self.B
        return altitude
    def _coordenadas(self):
        coordenadas = self.A + self.B
        return coordenadas
    # Retorna o peso da aresta
    def peso(self):
        peso = 3.6*500
        return peso