from itertools import product

def encontrar_anulables(gramatica):
    anulables = set()
    
    print("\n--- Buscando Símbolos Anulables ---")
    
    agregados_esta_iteracion = []
    for cabeza, alternativas in gramatica.items():
        if "" in alternativas:
            anulables.add(cabeza)
            agregados_esta_iteracion.append((cabeza, "tiene producción directa a ε"))
            
    iteracion = 1
    if agregados_esta_iteracion:
        print(f"Iteración 0:")
        for cabeza, motivo in sorted(agregados_esta_iteracion):
            print(f" - {cabeza} es anulable porque {motivo}")
            
    cambio = True
    while cambio:
        cambio = False
        agregados_esta_iteracion = []
        for cabeza, alternativas in gramatica.items():
            if cabeza in anulables:
                continue
                
            for alt in alternativas:
                if alt == "":
                    continue
                    
                todos_anulables = True
                for char in alt:
                    if char not in anulables:
                        todos_anulables = False
                        break
                        
                if todos_anulables:
                    anulables.add(cabeza)
                    agregados_esta_iteracion.append((cabeza, f"su cuerpo '{alt}' está formado solo por símbolos anulables"))
                    cambio = True
                    break
                    
        if agregados_esta_iteracion:
            print(f"Iteración {iteracion}:")
            for cabeza, motivo in sorted(agregados_esta_iteracion):
                print(f" - {cabeza} es anulable porque {motivo}")
        iteracion += 1
                    
    return anulables

def obtener_posiciones_anulables(cuerpo, anulables):
    posiciones = []
    for i, char in enumerate(cuerpo):
        if char in anulables:
            posiciones.append(i)
    return posiciones

def eliminar_epsilon(gramatica, anulables):
    nueva_gramatica = {}
    
    print("\n--- Construyendo Gramática sin ε ---")
    
    for cabeza, alternativas in sorted(gramatica.items()):
        for alt in sorted(list(alternativas)):
            if alt == "":
                continue
            posiciones = obtener_posiciones_anulables(alt, anulables)
            if len(posiciones) == len(alt) and len(alt) > 0:
                print(f"Nota: El cuerpo '{alt}' de la producción '{cabeza}' es completamente anulable.")

    for cabeza, alternativas in sorted(gramatica.items()):
        nueva_gramatica[cabeza] = set()
        
        for alt in sorted(list(alternativas)):
            if alt == "":
                print(f"\nProducción {cabeza} -> ε: descartada directamente.")
                continue
                
            posiciones = obtener_posiciones_anulables(alt, anulables)
            combinaciones_totales = 2 ** len(posiciones)
            
            print(f"\nProcesando {cabeza} -> '{alt}':")
            if posiciones:
                print(f" - Posiciones anulables: {posiciones}")
                print(f" - Explorando {combinaciones_totales} combinaciones:")
            else:
                print(f" - No tiene posiciones anulables. Se conserva directamente.")
            
            variantes = set()
            for combinacion in product([True, False], repeat=len(posiciones)):
                nueva_variante = ""
                idx_anulable = 0
                accion = []
                
                for i, char in enumerate(alt):
                    if i in posiciones:
                        conservar = combinacion[idx_anulable]
                        if conservar:
                            nueva_variante += char
                            accion.append("Conservar")
                        else:
                            accion.append("Quitar")
                        idx_anulable += 1
                    else:
                        nueva_variante += char
                        
                accion_str = ", ".join(accion) if accion else "Ninguna (sin anulables)"
                resultado_str = nueva_variante if nueva_variante != "" else "ε"
                
                if posiciones:
                    print(f"   * Combinación [{accion_str}] -> '{resultado_str}'")
                
                if nueva_variante == "":
                    print(f"     -> Variante vacía descartada.")
                elif nueva_variante in variantes:
                    print(f"     -> Variante '{nueva_variante}' descartada por duplicado.")
                else:
                    variantes.add(nueva_variante)
                    
            for variante in variantes:
                nueva_gramatica[cabeza].add(variante)
                
    if "S" in anulables:
        print("\nAviso: El símbolo inicial (S) es anulable. Al eliminar las producciones ε, se excluye la cadena vacía del lenguaje generado.")
        
    return nueva_gramatica
