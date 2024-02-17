from clases import *

def main():
    pontareas=Nodo("pontareas", 42.17646944251157, -8.499949199528857)
    pontevedra=Nodo("pontevedra", 42.43640646249162, -8.646261114788086)
    a1= Aeropuerto("santiago",42.89028498204115, -8.417720821165457,'SCQ')
    a2= Aeropuerto("madrid",40.49382107435963, -3.561814510964957,'MAD')
    conexion=Conexion(pontareas, pontevedra)
    conexion2=Conexion(a1,a2)
    print(conexion.distancia)
    print(conexion.medios_transporte)
    print(conexion2.distancia)
    print(conexion2.medios_transporte)

if __name__ == "__main__":
    main()