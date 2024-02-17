from clases import *

def main():
    nodos=[Nodo("oleiros", 43.34208844419752, -8.35115125406714),Nodo("pontevedra",42.42906091932056, -8.63078074971588),Nodo("nigran",42.13862307328924, -8.805517871019621)]
    #,Nodo("ponteareas",42.17579153763052, -8.502502935417787),Aeropuerto("santiago",42.89028498204115, -8.417720821165457,'SCQ')]
    
    grafo= Grafo()
    
    for nodo in nodos:
        grafo.nuevo_persona(nodo)
        
    grafo.conexiones_todas()
    

if __name__ == "__main__":
    main()