class Viaje:
    def __init__(self, nombre, destino):
        self.nombre = nombre
        self.destino = destino
        self.nodos = {}

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    