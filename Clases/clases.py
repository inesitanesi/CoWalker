from geopy import distance
import osmnx as ox
import pandas as pd
import numpy as np
import requests

class Nodo:
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.persona = 0
        #self.conexiones = {}  # Diccionario para almacenar las conexiones con otros nodos
        #Una función para añadir todas las conexiones
    
    def anadir_persona(self):
        self.persona+=1
    
    # def agregar_conexion(self, nodo_destino, distancia, medios_transporte):
    #     self.conexiones[nodo_destino] = {'distancia': distancia, 'medios_transporte': medios_transporte}

    def __str__(self):
        return f"Nodo: {self.nombre} - Latitud: {self.latitud} - Longitud: {self.longitud}"

class Aeropuerto(Nodo):
    def __init__(self, nombre, latitud, longitud, iata):
        super().__init__(nombre, latitud, longitud)
        self.iata = iata

class Conexion:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
        self.distancia = self.calcular_distancia()
        self.medios_transporte = self.calcular_consumo()

    def existeCamino(self, medio):
        if medio == 'avion':
            if isinstance(self.origen,Aeropuerto) and isinstance(self.destino,Aeropuerto):
                API_KEY = "CrSmr145BGGAxnDfiBsW1hoJiTY5"
                # Define the endpoint you want to access
                endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"

                params={
                    'originLocationCode': f'{self.origen.iata}',
                    'destinationLocationCode':f'{self.destino.iata}',
                    'departureDate':'2024-02-19',
                    'adults':'1',
                    'nonStop':'true',
                    'max':'1'
                }

                # Set up the request headers with your API credentials
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }

                # Make the GET request to the Amadeus API
                response = requests.get(endpoint, headers=headers,params=params)

                # Check if the request was successful
                if response.status_code == 200:
                    # Extract and print the response data
                    data = response.json()
                    if data['meta']['count']!=0:
                        return True
                    else:
                        return False
                else:
                    # Print the error message if the request was not successful
                    return False
            else:
                return False
        else:
            return False
        
    def calcular_distancia(self):
        origenData = (self.origen.latitud, self.origen.longitud)
        destinoData = (self.destino.latitud, self.destino.longitud)
        distancia = [-1,-1,-1,-1]        
        
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
            ruta = route_data["routes"][0]["distance"] / 1000  # Convert to kilometers
            
            if ruta <2:
                distancia[0]=ruta       #Permitimos andar
            else:
                distancia[0]=-1
            distancia[1]=ruta           #Añadimos distancia en coche
            #distancia[2]=ruta    
            
        else:
            print("Error:", response.status_code)
        
        ruta = distance.distance(origenData, destinoData).kilometers
        
        if self.existeCamino('tren'):
            distancia[2]=ruta
        else:
            distancia[2]=-1
            
        if self.existeCamino('avion'):
            distancia[3]=ruta
        else:
            distancia[3]=-1
            
        return distancia

    def calcular_consumo(self):
        d1 = {
            "walk": -1 if self.distancia[0] == -1 else 0,
            "coche": -1 if self.distancia[1] == -1 else 156 * self.distancia[1],
            #"bus": -1 if self.distancia[2] == -1 else 68 * self.distancia[2],
            "tren": -1 if self.distancia[2] == -1 else 14 * self.distancia[2],
            "avion": -1 if self.distancia[3] == -1 else 285 * self.distancia[3]
        }
        return d1
                  

class Grafo:
    def __init__(self):
        self.nodos = {}
        self.conexiones ={}        

    def nuevo_persona(self,nodo):
        nodo.anadir_persona()
        self.nodos[nodo.nombre] = nodo
        if not isinstance(nodo,Aeropuerto):
            self.anadir_aeropuertos(nodo,50*1000)
        #self.anadir_estaciones(nodo,20000)
        
    def conexiones_todas(self):
        for origen in self.nodos.values():
            for destino in self.nodos.values():
                if origen.nombre != destino.nombre:
                    self.conexiones[origen.nombre+'-'+destino.nombre]=Conexion(origen,destino)
                    print(f'{origen.nombre+'-'+destino.nombre}: ')
                    print(self.conexiones[origen.nombre+'-'+destino.nombre].medios_transporte)

    
    def agregar_nodo(self, nodo):
        self.nodos[nodo.nombre] = nodo

    def obtener_nodo(self, nombre):
        return self.nodos.get(nombre)

    def agregar_conexion(self, nodo):
        self.conexion[self.conexion.nombre] = nodo

    def obtener_conexion(self, nombre):
        return self.conexion.get(nombre)
    
    def obtener_conexiones_origen(self,nodo):
        data =[]
        for conex in self.conexiones.values():
            if conex.origen == nodo.nombre:
                data.append(conex)
        return data

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
        df['iata'] = df['iata'].replace({'': np.nan})     
        df = df.dropna(subset=['iata']) #Buscamos solo aeropuertos con IATA
        
        for iter,place in df.iterrows():
            aeropuerto = Aeropuerto(place['name'],place['geometry'].centroid.y,place['geometry'].centroid.x,place['iata'])
            self.agregar_nodo(aeropuerto)

    #Función para añadir las estaciones cercanas a un nodo
    def anadir_estaciones(self, origen, distancia):
        tags = {"public_transport": "station"}         #Tipo de servicio
        places = ox.features_from_point((origen.latitud, origen.longitud), tags, dist=distancia)   #Recuperamos datos
        df = pd.DataFrame(places)
        for iter,place in df.iterrows():
            estacion = Nodo(place['name'], place['geometry'].centroid.y,place['geometry'].centroid.x)
            self.agregar_nodo(estacion)

    
        
        

    

