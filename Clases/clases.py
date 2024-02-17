from geopy import distance
import osmnx as ox
import pandas as pd
import numbpy as np
import json

class Nodo:
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        #self.conexiones = {}  # Diccionario para almacenar las conexiones con otros nodos
        #Una función para añadir todas las conexiones

    # def agregar_conexion(self, nodo_destino, distancia, medios_transporte):
    #     self.conexiones[nodo_destino] = {'distancia': distancia, 'medios_transporte': medios_transporte}

    def __str__(self):
        return f"Nodo: {self.nombre} - Latitud: {self.latitud} - Longitud: {self.longitud}"

class Aeropuerto(Nodo):
    def __init__(self, nombre, latitud, longitud, iata):
        super().__init__(nombre, latitud, longitud)
        self.iata = iata

class Conexion:
    def __init__(self, origen, destino, medio_transporte):
        self.origen = origen
        self.destino = destino
        self.medio_transporte = medio_transporte
        self.distancia = calcular_distancia()
        self.consumo = calcular_consumo()
        
    def calcular_distancia(self):
        origenData = (self.origen.latitud, self.origen.longitud)
        destinoData = (self.destino.latitud, self.destino.longitud)
        distancia = distance.distance(origenData, destinoData).kilometers
        return distancia

    def calcular_consumo(self):
        

class Grafo:
    def __init__(self):
        self.nodos = {}
        self.conexiones ={}

    def agregar_nodo(self, nodo):
        self.nodos[nodo.nombre] = nodo

    def obtener_nodo(self, nombre):
        return self.nodos.get(nombre)

    def agregar_conexion(self, nodo):
        self.conexion[conexion.nombre] = nombre

    def obtener_conexion(self, nombre):
        return self.conexion.get(nombre)

    def __str__(self):
        return f"Grafo con {len(self.nodos)} nodos"

    #Función para añadir todos los aeropuertos cercanos a un nodo
    def anadir_aeropuertos(self, origen, distancia):
        """
        origen: Nodo(nombre, latitud, longitud)
        distancia: int (radio de busqueda en metros)
        """
        tags = {"aeroway": "aerodrome"}         #Tipo de servicio
        places = ox.features_from_point((origen.latitud, origen.longitud), tags, dist=distancia)   #Recuperamos datos
        df = pd.DataFrame(places)
        df['ref'] = df['ref'].replace({'': np.nan})     
        df = df.dropna(subset=['ref']) #Buscamos solo aeropuertos con IATA
        
        for place in df:
            aeropuerto = Aeropuerto(place['name'],place['geometry'].centroid.y,place['geometry'].centroid.x,place['ref'])
            agregar_nodo(aeropuerto)

    #Función para añadir las estaciones cercanas a un nodo
    def anadir_estaciones(self, origen, distancia):
        tags = {"public_transport": "station"}         #Tipo de servicio
        places = ox.features_from_point((origen.latitud, origen.longitud), tags, dist=distancia)   #Recuperamos datos
        df = pd.DataFrame(places)
        for place in df:
            estacion = Nodo(place['name'], place['geometry'].centroid.y,place['geometry'].centroid.x)
            agregar_nodo(estacion)

    
        
        

    

