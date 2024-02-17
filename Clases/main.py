from clases import *

def main():
    coruna=Nodo("coruna", 43.36223966912647, -8.411158701710125)
    oleiros=Nodo("madrid",40.49420298981081, -3.7107454048199218)
    a1= Aeropuerto("santiago",42.89028498204115, -8.417720821165457,'SCQ')
    a2= Aeropuerto("madrid",40.49382107435963, -3.561814510964957,'MAD')
    
    grafo= Grafo()
    
    grafo.nuevo_persona(coruna)
    grafo.nuevo_persona(oleiros)
    grafo.conexiones_todas()
    print(grafo.nodos)
    print(grafo.conexiones)    

if __name__ == "__main__":
    main()