from geopy import distance
import osmnx as ox
import pandas as pd
import numpy as np
import osrm

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
        
        
        if (self.medio_transporte=='coche'):
        
            osrm_url = "http://router.project-osrm.org/route/v1/driving/{},{};{},{}?steps=true"

            # Format the URL with the coordinates of the starting and ending points
            url = osrm_url.format(origenData[1], origenData[0], destinoData[1], destinoData[0])

            # Send a GET request to the OSRM server
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the route information from the response
                route_data = response.json()
                
                # Extract the distance and duration of the route
                distancia = route_data["routes"][0]["distance"] / 1000  # Convert to kilometers
                
                return distancia
            else:
                print("Error:", response.status_code)
        else:   
            distancia = distance.distance(origenData, destinoData).kilometers
            return distancia

    def calcular_consumo(self):
        if self.medio_transporte == "coche":
            dato=156
        elif self.medio_transporte == "tren":
            dato=14
        elif self.medio_transporte == "avion":
            dato=285
        elif self.medio_transporte == "bus":
            dato=68
        elif self.medio_transporte == "walk":
            dato=0
        return dato*self.distancia
        

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

    
        
        

    

