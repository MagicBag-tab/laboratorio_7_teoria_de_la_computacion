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

def generar_variantes(cuerpo, anulables):
    pass

def eliminar_epsilon(gramatica):
    pass
