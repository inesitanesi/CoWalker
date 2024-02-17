from clases import *

def main():
    coruna=Nodo("coruna", 43.36223966912647, -8.411158701710125)
    pontevedra=Nodo("pontevedra", 43.36223966912647, -8.411158701710125)
    a1= Aeropuerto("santiago",42.89028498204115, -8.417720821165457,'SCQ')
    a2= Aeropuerto("madrid",40.49382107435963, -3.561814510964957,'MAD')
    
    grafo= Grafo()
    
    grafo.nuevo_persona(coruna)
    grafo.conexiones_todas()
    print(grafo.conexiones)    

if __name__ == "__main__":
    main()