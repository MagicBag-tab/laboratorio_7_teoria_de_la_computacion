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
                if texto:
                    lineas.append((num_linea, texto))
    except Exception as e:
        print(f"Error al leer el archivo '{ruta}': {e}")
        return None
        
    if not lineas:
        print(f"Aviso: El archivo '{ruta}' está vacío.")
        return None
        
    return lineas

def validar_linea(numero_linea, linea):
    if '->' not in linea and '→' not in linea:
        print(f"Error en la línea {numero_linea}: Falta la flecha.")
        return False
        
    separador = '->' if '->' in linea else '→'
    partes = linea.split(separador)
    
    if len(partes) != 2:
        print(f"Error en la línea {numero_linea}: Hay más de una flecha.")
        return False
        
    cabeza = partes[0].strip()
    cuerpo = partes[1].strip()
    
    if len(cabeza) != 1 or not cabeza.isupper() or not cabeza.isalpha():
        print(f"Error en la línea {numero_linea}: La cabeza '{cabeza}' debe ser una sola letra mayúscula.")
        return False
        
    if not cuerpo:
        print(f"Error en la línea {numero_linea}: El cuerpo está vacío.")
        return False
        
    alternativas = cuerpo.split('|')
    for alt in alternativas:
        alt_strip = alt.strip()
        
        if not alt_strip:
            print(f"Error en la línea {numero_linea}: Falta una alternativa.")
            return False
            
        alt_sin_espacios = alt_strip.replace(' ', '')
        
        if 'ε' in alt_sin_espacios or 'ϵ' in alt_sin_espacios:
            if len(alt_sin_espacios) > 1:
                print(f"Error en la línea {numero_linea}: ε está mezclada con otro símbolo.")
                return False
                
        for char in alt_sin_espacios:
            if not (char.isalpha() or char.isdigit() or char in ('ε', 'ϵ')):
                print(f"Error en la línea {numero_linea}: Símbolo no permitido '{char}'.")
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
