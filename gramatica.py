from afn import Estado, AFN, EPSILON

def construir_afn_validador():
    q_ini = Estado(0)
    q_head = Estado(1)
    q_dash = Estado(2)
    q_arrow = Estado(3)
    q_body_sym = Estado(4)
    q_body_eps = Estado(5)
    q_pipe = Estado(6)
    q_final = Estado(7, es_aceptacion=True)
    
    estados = [q_ini, q_head, q_dash, q_arrow, q_body_sym, q_body_eps, q_pipe, q_final]
    
    letras_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letras_minusculas = "abcdefghijklmnopqrstuvwxyz"
    digitos = "0123456789"
    simbolos_regulares = letras_mayusculas + letras_minusculas + digitos
    
    q_ini.agregar_transicion(q_ini, " ")
    for c in letras_mayusculas:
        q_ini.agregar_transicion(q_head, c)
        
    q_head.agregar_transicion(q_head, " ")
    q_head.agregar_transicion(q_dash, "-")
    q_dash.agregar_transicion(q_arrow, ">")
    q_head.agregar_transicion(q_arrow, "→")
    
    q_arrow.agregar_transicion(q_arrow, " ")
    q_arrow.agregar_transicion(q_body_eps, "ε")
    q_arrow.agregar_transicion(q_body_eps, "ϵ")
    
    q_body_eps.agregar_transicion(q_body_eps, " ")
    q_body_eps.agregar_transicion(q_pipe, "|")
    
    for c in simbolos_regulares:
        q_arrow.agregar_transicion(q_body_sym, c)
        q_body_sym.agregar_transicion(q_body_sym, c)
        
    q_body_sym.agregar_transicion(q_body_sym, " ")
    q_body_sym.agregar_transicion(q_pipe, "|")
    
    q_pipe.agregar_transicion(q_pipe, " ")
    for c in simbolos_regulares:
        q_pipe.agregar_transicion(q_body_sym, c)
        
    q_pipe.agregar_transicion(q_body_eps, "ε")
    q_pipe.agregar_transicion(q_body_eps, "ϵ")
    
    q_body_sym.agregar_transicion(q_final, EPSILON)
    q_body_eps.agregar_transicion(q_final, EPSILON)
    q_final.agregar_transicion(q_final, " ")
    
    return AFN(q_ini, q_final, estados)

validador_afn = construir_afn_validador()

def validar_linea(numero_linea, linea):
    aceptada, _ = validador_afn.simular(linea)
    if not aceptada:
        print(f"Error en la línea {numero_linea}: Rechazada por el Analizador Léxico (Autómata AFN).")
        return False
    return True

def interpretar_gramatica(lineas):
    gramatica = {}
    for num_linea, linea in lineas:
        if not validar_linea(num_linea, linea):
            return None
            
        separador = '->' if '->' in linea else '→'
        cabeza, cuerpo = linea.split(separador, 1)
        cabeza = cabeza.strip()
        cuerpo = cuerpo.strip()
        
        if cabeza not in gramatica:
            gramatica[cabeza] = set()
            
        alternativas = cuerpo.split('|')
        for alt in alternativas:
            alt_limpia = alt.strip().replace(' ', '')
            
            if alt_limpia in ('ε', 'ϵ'):
                gramatica[cabeza].add("")
            else:
                gramatica[cabeza].add(alt_limpia)
                
    return gramatica

def mostrar_gramatica(gramatica):
    if not gramatica:
        print("La gramática está vacía.")
        return
        
    for cabeza, alternativas in gramatica.items():
        alts_lista = []
        for alt in alternativas:
            if alt == "":
                alts_lista.append("ε")
            else:
                alts_lista.append(alt)
                
        alts_str = ' | '.join(sorted(alts_lista))
        print(f"{cabeza} -> {alts_str}")
