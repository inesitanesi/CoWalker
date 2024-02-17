class Viaje:
    def __init__(self):
        
        self.nodos = {}
        
    def set_nombre(self,nombre):
        self.nombre=nombre
        
    def set_destino(self,destino):
        self.destino=destino

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    