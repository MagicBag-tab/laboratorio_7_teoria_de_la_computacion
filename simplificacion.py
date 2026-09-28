from itertools import product

def encontrar_anulables(gramatica):
    anulables = set()
    
    for cabeza, alternativas in gramatica.items():
        if "" in alternativas:
            anulables.add(cabeza)
            
    cambio = True
    while cambio:
        cambio = False
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
                    cambio = True
                    break
                    
    return anulables

def obtener_posiciones_anulables(cuerpo, anulables):
    posiciones = []
    for i, char in enumerate(cuerpo):
        if char in anulables:
            posiciones.append(i)
    return posiciones

def generar_variantes(cuerpo, anulables):
    if cuerpo == "":
        return set(), True, []
        
    posiciones = obtener_posiciones_anulables(cuerpo, anulables)
    completamente_anulable = (len(posiciones) == len(cuerpo))
    
    variantes = set()
    
    for combinacion in product([True, False], repeat=len(posiciones)):
        nueva_variante = ""
        idx_anulable = 0
        
        for i, char in enumerate(cuerpo):
            if i in posiciones:
                conservar = combinacion[idx_anulable]
                if conservar:
                    nueva_variante += char
                idx_anulable += 1
            else:
                nueva_variante += char
                
        if nueva_variante != "":
            variantes.add(nueva_variante)
            
    return variantes, completamente_anulable, posiciones

def eliminar_epsilon(gramatica, anulables):
    nueva_gramatica = {}
    
    for cabeza, alternativas in gramatica.items():
        nueva_gramatica[cabeza] = set()
        
        for alt in alternativas:
            if alt == "":
                continue
                
            variantes, _, _ = generar_variantes(alt, anulables)
            for variante in variantes:
                nueva_gramatica[cabeza].add(variante)
                
    if "S" in anulables:
        print("Aviso: El símbolo inicial (S) es anulable. Al eliminar las producciones ε, se excluye la cadena vacía del lenguaje generado.")
        
    return nueva_gramatica
