def encontrar_anulables(gramatica):
    """
    Identifica los símbolos que pueden generar ε (cadena vacía).
    """
    anulables = set()
    pendientes = []
    dependientes = {}
    producciones = []
    restantes = []

    for cabeza, alternativas in gramatica.items():
        for cuerpo in alternativas:
            simbolos = set(cuerpo) - {'ε', 'ϵ'}
            if not simbolos:
                if cabeza not in anulables:
                    anulables.add(cabeza)
                    pendientes.append(cabeza)
            elif simbolos.issubset(gramatica):
                indice = len(producciones)
                producciones.append(cabeza)
                restantes.append(len(simbolos))
                for simbolo in simbolos:
                    dependientes.setdefault(simbolo, []).append(indice)

    while pendientes:
        simbolo = pendientes.pop()
        for indice in dependientes.get(simbolo, ()):
            restantes[indice] -= 1
            cabeza = producciones[indice]
            if restantes[indice] == 0 and cabeza not in anulables:
                anulables.add(cabeza)
                pendientes.append(cabeza)

    return anulables

def generar_variantes(cuerpo, anulables):
    """
    Obtiene las combinaciones de un cuerpo de producción al eliminar símbolos anulables.
    """
    # TODO: Implementar lógica
    pass

def eliminar_epsilon(gramatica):
    """
    Construye y devuelve la gramática resultante sin producciones ε.
    """
    # TODO: Implementar lógica
    pass
