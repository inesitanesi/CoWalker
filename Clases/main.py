import clases

def main():
    pontareas=Nodo("pontareas", 42.17646944251157, -8.499949199528857)
    pontevedra=Nodo("pontevedra", 42.43640646249162, -8.646261114788086)
    conexion=Conexion(pontareas, pontevedra, "tren")
    print(conexion.consumo)

if __name__ == "__main__":
    main()