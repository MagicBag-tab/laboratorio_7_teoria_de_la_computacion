from dataclasses import dataclass, field

EPSILON = "nobody"

@dataclass
class Transicion:
    destino: "Estado"
    simbolo: str = EPSILON

@dataclass(eq=False)
class Estado:
    id: int
    transiciones: list = field(default_factory=list)
    es_aceptacion: bool = False

    def agregar_transicion(self, destino: "Estado", simbolo: str = EPSILON):
        self.transiciones.append(Transicion(destino, simbolo))

class AFN:
    def __init__(self, inicial: Estado, aceptacion: Estado, estados: list):
        self.inicial = inicial
        self.aceptacion = aceptacion
        self.estados = estados

    def transiciones_epsilon(self, estados):
        cierre = set(estados)
        pila = list(estados)
        while pila:
            estado = pila.pop()
            for transicion in estado.transiciones:
                if transicion.simbolo == EPSILON and transicion.destino not in cierre:
                    cierre.add(transicion.destino)
                    pila.append(transicion.destino)
        return cierre

    def mover(self, estados, simbolo):
        destinos = set()
        for estado in estados:
            for transicion in estado.transiciones:
                if transicion.simbolo == simbolo:
                    destinos.add(transicion.destino)
        return self.transiciones_epsilon(destinos)

    def simular(self, cadena):
        actuales = self.transiciones_epsilon({self.inicial})
        for simbolo in cadena:
            actuales = self.mover(actuales, simbolo)
            if not actuales:
                break
        return self.aceptacion in actuales, []
