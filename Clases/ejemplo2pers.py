from jsonschema import validate
import json
import heapq

def validar_datos(schema_file, data_file):
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

def dijkstra(nodos, conexiones, start):
    dijkstra_graph = {}
    for conexion in conexiones:
        orig_nodo = conexion['nodo_origen']
        dest_nodo = conexion['nodo_destino']
        emision = min(filter(lambda x: x != -1, conexion['medios_transporte']))

        if orig_nodo not in dijkstra_graph:
            dijkstra_graph[orig_nodo] = {}
        if dest_nodo not in dijkstra_graph:
            dijkstra_graph[dest_nodo] = {}
        dijkstra_graph[orig_nodo][dest_nodo] = emision
        dijkstra_graph[dest_nodo][orig_nodo] = emision
    
    heap = [(0, start)]
    emisiones = {start: (0, [start])}  # Mantenemos una lista de nodos visitados hasta ahora
    while heap:
        (emision, node) = heapq.heappop(heap)
        if node in dijkstra_graph:            
            for vecino, peso in dijkstra_graph[node].items():
                
                nueva_emision = emision + peso
                if vecino not in emisiones or nueva_emision < emisiones[vecino][0]:
                    nuevo_camino = emisiones[node][1] + [vecino]  # Nuevo camino
                    emisiones[vecino] = (nueva_emision, nuevo_camino)
                    heapq.heappush(heap, (nueva_emision, vecino))
    return emisiones

def funcion_opt(nodos, conexiones, start_node, end_node):
    emisiones_minimas = dijkstra(nodos, conexiones, start_node)
    emision_minima, shortest_path = emisiones_minimas[end_node]
    
    # Obtener los medios de transporte utilizados en cada conexión del camino óptimo
    medios_transporte_camino = []
    for i in range(len(shortest_path) - 1):
        origen = shortest_path[i]
        destino = shortest_path[i+1]
        medio_transporte = None
        for conexion in conexiones:
            if (conexion['nodo_origen'] == origen and conexion['nodo_destino'] == destino) or \
               (conexion['nodo_origen'] == destino and conexion['nodo_destino'] == origen):
                # Obtener el índice del medio de transporte utilizado
                medio_transporte = conexion['medios_transporte'].index(min(filter(lambda x: x != -1, conexion['medios_transporte'])))
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


schema = 'schema-json.json'
data='ejemplo.json'
data=validar_datos(schema, data)

start_node = "Ines"
end_node = "Aeropuerto Santiago"
co2_optimized_distance, medios_transporte_camino = funcion_opt(data["nodos"], data["conexiones"], start_node, end_node)
print("Distancia óptima para Inés:", co2_optimized_distance)
for origen, destino, medios_transporte in medios_transporte_camino:
    if medios_transporte == 0:
        print(f"De {origen} a {destino}: andando")
    elif medios_transporte == 1:
        print(f"De {origen} a {destino}: coche")
    elif medios_transporte == 2:
        print(f"De {origen} a {destino}: tren")
    elif medios_transporte == 3:
        print(f"De {origen} a {destino}: avión")


start_node = "Rober"
co2_optimized_distance, medios_transporte_camino = funcion_opt(data["nodos"], data["conexiones"], start_node, end_node)
print("Distancia óptima para Rober:", co2_optimized_distance)
for origen, destino, medios_transporte in medios_transporte_camino:
    if medios_transporte == 0:
        print(f"De {origen} a {destino}: andando")
    elif medios_transporte == 1:
        print(f"De {origen} a {destino}: coche")
    elif medios_transporte == 2:
        print(f"De {origen} a {destino}: tren")
    elif medios_transporte == 3:
        print(f"De {origen} a {destino}: avión")