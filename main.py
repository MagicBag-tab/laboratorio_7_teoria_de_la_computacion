from lector import leer_archivo, interpretar_gramatica, mostrar_gramatica
from simplificacion import encontrar_anulables, generar_variantes, eliminar_epsilon

def main():
    
    ruta_archivo = "gramaticas/gramatica1.txt"
    print(f"\nIntentando leer '{ruta_archivo}'...")
    
    lineas = leer_archivo(ruta_archivo)
    if lineas is None:
        return
        
    gramatica = interpretar_gramatica(lineas)
    if not gramatica:
        print("No se pudo extraer ninguna producción válida de la gramática.")
        return
        
    print("\nGramática Original leída:")
    mostrar_gramatica(gramatica)


if __name__ == "__main__":
    main()
