import os

def leer_archivo(ruta):

    if not os.path.exists(ruta):
        print(f"Error: El archivo '{ruta}' no existe.")
        return None
    
    lineas = []
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            for num_linea, linea in enumerate(f, 1):
                texto = linea.strip()
                if texto and not texto.startswith('#'):
                    lineas.append((num_linea, texto))
    except Exception as e:
        print(f"Error al leer el archivo '{ruta}': {e}")
        return None
        
    if not lineas:
        print(f"Aviso: El archivo '{ruta}' está vacío o no contiene producciones válidas.")
        return None
        
    return lineas

def validar_linea(numero_linea, linea):

    if '->' not in linea and '→' not in linea:
        print(f"Error en la línea {numero_linea}: Falta el operador de producción ('->' o '→').")
        return False
        
    separador = '->' if '->' in linea else '→'
    partes = linea.split(separador)
    
    if len(partes) != 2:
        print(f"Error en la línea {numero_linea}: Hay más de un operador de producción en la misma línea.")
        return False
        
    cabeza, cuerpo = partes[0].strip(), partes[1].strip()
    
    if len(cabeza) != 1 or not cabeza.isupper() or not cabeza.isalpha():
        print(f"Error en la línea {numero_linea}: El lado izquierdo '{cabeza}' debe ser un único símbolo No Terminal (una letra mayúscula).")
        return False
        
    if not cuerpo:
        print(f"Error en la línea {numero_linea}: El cuerpo de la producción está vacío (use ε o ϵ explícitamente para la cadena vacía).")
        return False
        
    return True

def interpretar_gramatica(lineas):

    gramatica = {}
    for num_linea, linea in lineas:
        if not validar_linea(num_linea, linea):
            print(f"Se omitirá la línea {num_linea} debido a errores de formato.")
            continue
            
        separador = '->' if '->' in linea else '→'
        cabeza, cuerpo = linea.split(separador, 1)
        cabeza = cabeza.strip()
        cuerpo = cuerpo.strip()
        
        if cabeza not in gramatica:
            gramatica[cabeza] = []
            
        alternativas = cuerpo.split('|')
        for alt in alternativas:
            alt = alt.strip()
            simbolos = []
            
            if alt in ('ε', 'ϵ'):
                simbolos.append('ε')
            else:
                alt_sin_espacios = alt.replace(' ', '')
                for char in alt_sin_espacios:
                    if char in ('ε', 'ϵ'):
                        simbolos.append('ε')
                    else:
                        simbolos.append(char)
                        
            if simbolos not in gramatica[cabeza]:
                gramatica[cabeza].append(simbolos)
                
    return gramatica

def mostrar_gramatica(gramatica):

    if not gramatica:
        print("La gramática está vacía.")
        return
        
    for cabeza, alternativas in gramatica.items():
        alts_str = ' | '.join([''.join(alt) for alt in alternativas])
        print(f"{cabeza} -> {alts_str}")
