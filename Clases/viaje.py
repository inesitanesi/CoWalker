# CoWalker
# Copyright (c) 2024, Elena Fernández del Sel, Nicolás Fernández Otero, Roberto Tato Lage, Inés Quintana Raña
# SPDX-License-Identifier: MIT

import json
import heapq
from jsonschema import validate
from Clases.clases import *

class Viaje:
    def __init__(self):
        self.caminos=[]
        self.nodos = []
        
    def set_nombre(self,nombre):
        self.nombre=nombre
        
    def set_destino(self,destino):
        self.destino=destino

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)


    def validar_datos(self, schema_file, data_file):
        # Cargamos el esquema
        try:
            with open(schema_file, 'r') as schema_file:
                schema = json.load(schema_file)
        except Exception as e:
            print("Error al cargar el esquema:", e)
            raise
        
        # Cargamos los datos
        try:
            with open(data_file, 'r') as data_file:
                data = json.load(data_file)
        except Exception as e:
            print("Error al cargar los datos:", e)
            raise
        
        # Validamos los datos contra el esquema
        try:
            validate(instance=data, schema=schema)
            print("Los datos son válidos según el esquema.")
        except Exception as e:
            print("Error de validación:", e)
        return data

    def dijkstra(self, nodos, conexiones, start):
        dijkstra_graph = {}
        for conexion in conexiones.values():
            orig_nodo = conexion.origen.nombre
            dest_nodo = conexion.destino.nombre
            emision = min(filter(lambda x: x != -1, conexion.medios_transporte.values()))

            if orig_nodo not in dijkstra_graph:
                dijkstra_graph[orig_nodo] = {}
            if dest_nodo not in dijkstra_graph:
                dijkstra_graph[dest_nodo] = {}
            dijkstra_graph[orig_nodo][dest_nodo] = emision
            dijkstra_graph[dest_nodo][orig_nodo] = emision
        print(dijkstra_graph)
        heap = [(0, start)]
        emisiones = {start: (0, [start])}  # Mantenemos una lista de nodos visitados hasta ahora
        while heap:
            (emision, node) = heapq.heappop(heap)
            print(node)
            if node in dijkstra_graph:            
                for vecino, peso in dijkstra_graph[node].items():
                    
                    nueva_emision = emision + peso
                    if vecino not in emisiones or nueva_emision < emisiones[vecino][0]:
                        nuevo_camino = emisiones[node][1] + [vecino]  # Nuevo camino
                        emisiones[vecino] = (nueva_emision, nuevo_camino)
                        heapq.heappush(heap, (nueva_emision, vecino))
        return emisiones

    def funcion_opt(self, nodos, conexiones, start_node, end_node):
        emisiones_minimas = self.dijkstra(nodos, conexiones, start_node)
        print(emisiones_minimas)
        emision_minima, shortest_path = emisiones_minimas[end_node]
        
        # Obtener los medios de transporte utilizados en cada conexión del camino óptimo
        medios_transporte_camino = []
        for i in range(len(shortest_path) - 1):
            origen = shortest_path[i]
            destino = shortest_path[i+1]
            medio_transporte = None
            for conexion in conexiones.values():
                if (conexion.origen.nombre == origen and conexion.destino.nombre == destino) or \
                (conexion.origen.nombre == destino and conexion.destino.nombre == origen):
                    # Obtener el índice del medio de transporte utilizado
                    medio_transporte = list(conexion.medios_transporte.values()).index(min(filter(lambda x: x != -1, conexion.medios_transporte.values())))
                    medios_transporte_camino.append((origen, destino, medio_transporte))
                    
                    # Modificar el costo si dos personas comparten un coche
                    #if medio_transporte == 1:  # Si el medio de transporte es el coche
                        # Verificar si hay más de una persona en el nodo
                    #    num_personas_nodo_origen = next((nodo["persona"] for nodo in nodos if nodo["nombre"] == origen), None)
                    #    num_personas_nodo_destino = next((nodo["persona"] for nodo in nodos if nodo["nombre"] == destino), None)
                    #    if num_personas_nodo_origen == 2 and num_personas_nodo_destino == 2:
                            # Si dos personas comparten un coche, dividir el costo por la mitad
                    #        conexion['medios_transporte'][1] /= 2
                    #break
        print("Camino óptimo:", shortest_path)  # Imprimir el camino óptimo
        return emision_minima, medios_transporte_camino


    # schema = 'schema-json.json'
    # data='ejemplo.json'
    # data=validar_datos(schema, data)

    def ejecutar(self):
        start_node = self.nodos
        end_node = self.destino
        grafo=Grafo()
        grafo.nuevo_persona(end_node)
        end_node = self.destino.nombre
        for nodo in start_node:
            grafo.nuevo_persona(nodo)
        grafo.conexiones_todas()
        for nodo in start_node:
            camino=""
            co2_optimized_distance, medios_transporte_camino = self.funcion_opt(grafo.nodos,grafo.conexiones, nodo.nombre, end_node)
            print(co2_optimized_distance)
            camino+=f"Consumo óptimo para {nodo.nombre}: "+str(co2_optimized_distance)+'\n'
            for origen, destino, medios_transporte in medios_transporte_camino:
                if medios_transporte == 0:
                    camino+=f"De {origen} a {destino}: andando -> \n"
                elif medios_transporte == 1:
                    camino+=f"De {origen} a {destino}: coche -> \n"
                elif medios_transporte == 2:
                    camino+=f"De {origen} a {destino}: tren -> \n"
                elif medios_transporte == 3:
                    camino+=f"De {origen} a {destino}: avión -> \n"
            self.caminos.append(camino)


        