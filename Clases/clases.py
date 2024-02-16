class Nodo:
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.conexiones = {}  # Diccionario para almacenar las conexiones con otros nodos

    def agregar_conexion(self, nodo_destino, distancia, medios_transporte):
        self.conexiones[nodo_destino] = {'distancia': distancia, 'medios_transporte': medios_transporte}

    def __str__(self):
        return f"Nodo: {self.nombre} - Latitud: {self.latitud} - Longitud: {self.longitud}"

class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, nodo):
        self.nodos[nodo.nombre] = nodo

    def obtener_nodo(self, nombre):
        return self.nodos.get(nombre)

    def __str__(self):
        return f"Grafo con {len(self.nodos)} nodos"