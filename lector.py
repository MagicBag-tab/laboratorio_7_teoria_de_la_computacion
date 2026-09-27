import re

def leer_gramatica(ruta):
    """
    Lee una gramática desde un archivo de texto.
    
    Reglas soportadas:
    - Una producción por línea, con símbolos separados por '|'
    - Una letra mayúscula representa un no terminal.
    - Las minúsculas y los dígitos representan terminales.
    - Acepta '->' y '→'.
    - Acepta 'ε' y 'ϵ' como formas de escribir la cadena vacía.
    
    Retorna:
        Un diccionario donde la clave es el no terminal y el valor
        es una lista de alternativas, donde cada alternativa es una lista de símbolos.
    """
    gramatica = {}
    
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
                
            if '->' in linea:
                cabeza, cuerpo = linea.split('->', 1)
            elif '→' in linea:
                cabeza, cuerpo = linea.split('→', 1)
            else:
                continue
                
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
                    alt = alt.replace(' ', '')
                    for char in alt:
                        if char == 'ϵ':
                            simbolos.append('ε')
                        else:
                            simbolos.append(char)
                            
                gramatica[cabeza].append(simbolos)
                
    return gramatica

def es_no_terminal(simbolo):
    return simbolo.isupper() and simbolo.isalpha()

def es_terminal(simbolo):
    return (simbolo.islower() and simbolo.isalpha()) or simbolo.isdigit()

def imprimir_gramatica(gramatica):
    for no_terminal, alternativas in gramatica.items():
        str_alternativas = ' | '.join([''.join(alt) for alt in alternativas])
        print(f"{no_terminal} -> {str_alternativas}")
