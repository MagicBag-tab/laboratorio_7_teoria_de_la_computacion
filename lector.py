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
