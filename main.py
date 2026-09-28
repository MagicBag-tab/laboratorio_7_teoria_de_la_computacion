from lector import leer_archivo
from gramatica import interpretar_gramatica, mostrar_gramatica
from simplificacion import encontrar_anulables, generar_variantes

def main():
    print("=== Simplificación de Gramáticas ===")
    
    ruta_archivo = "gramaticas/gramatica1.txt"
    print(f"\nLeyendo '{ruta_archivo}'...")
    
    lineas = leer_archivo(ruta_archivo)
    if lineas is None:
        return
        
    gramatica = interpretar_gramatica(lineas)
    if gramatica is None:
        print("\nLa validación falló. Se detiene la ejecución antes de transformar la gramática.")
        return
        
    print("\nGramática original:")
    mostrar_gramatica(gramatica)
    
    anulables = encontrar_anulables(gramatica)
    print(f"\nSímbolos anulables encontrados: {anulables}")
    
    print("\n--- Análisis de Cuerpos ---")
    for cabeza, alternativas in gramatica.items():
        for alt in alternativas:
            if alt == "":
                continue
            variantes, completo, posiciones = generar_variantes(alt, anulables)
            print(f"Cuerpo '{alt}': Posiciones anulables {posiciones}, Completamente anulable: {completo}")
            print(f" -> Variantes generadas: {variantes}")

if __name__ == "__main__":
    main()
