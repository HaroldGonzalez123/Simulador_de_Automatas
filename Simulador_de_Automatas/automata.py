class Automata:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.estado_inicial = None
        self.estados_finales = set()
        self.transiciones = {}

    def agregar_estado(self, estado):
        self.estados.add(estado)

    def agregar_simbolo(self, simbolo):
        self.alfabeto.add(simbolo)

    def definir_inicial(self, estado):
        if estado not in self.estados:
            raise ValueError("El estado inicial debe existir.")
        self.estado_inicial = estado

    def agregar_final(self, estado):
        if estado not in self.estados:
            raise ValueError("El estado final debe existir.")
        self.estados_finales.add(estado)

    def agregar_transicion(self, origen, simbolo, destino):
        if origen not in self.estados:
            raise ValueError("El estado de origen no existe.")

        if destino not in self.estados:
            raise ValueError("El estado de destino no existe.")

        if simbolo != "ε" and simbolo not in self.alfabeto:
            raise ValueError("El símbolo no pertenece al alfabeto.")

        self.transiciones.setdefault((origen, simbolo), set()).add(destino)

    def simular(self, cadena):
        if self.estado_inicial is None:
            raise ValueError("No se ha definido el estado inicial.")

        estados_actuales = self.epsilon_closure({self.estado_inicial})

        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False

            nuevos_estados = set()

            for estado in estados_actuales:
                clave = (estado, simbolo)

                if clave in self.transiciones:
                    nuevos_estados.update(self.transiciones[clave])

            if not nuevos_estados:
                return False

            estados_actuales = self.epsilon_closure(nuevos_estados)

        return bool(estados_actuales & self.estados_finales)
    
    def epsilon_closure(self, estados):
        clausura = set(estados)
        pendientes = list(estados)

        while pendientes:
            estado = pendientes.pop()
            clave = (estado, "ε")

            if clave in self.transiciones:
                for destino in self.transiciones[clave]:
                    if destino not in clausura:
                        clausura.add(destino)
                        pendientes.append(destino)

        return clausura

    def mover(self, estados, simbolo):
        destinos = set()

        for estado in estados:
            clave = (estado, simbolo)

            if clave in self.transiciones:
                destinos.update(self.transiciones[clave])

        return destinos 

    def convertir_a_afd(self):
        afd = Automata()

        estado_inicial = frozenset(
            self.epsilon_closure({self.estado_inicial})
        )

        pendientes = [estado_inicial]
        visitados = set()

        nombre_inicial = "{" + ",".join(sorted(estado_inicial)) + "}"
        afd.agregar_estado(nombre_inicial)
        afd.definir_inicial(nombre_inicial)

        while pendientes:
            conjunto_actual = pendientes.pop()

            if conjunto_actual in visitados:
                continue

            visitados.add(conjunto_actual)

            nombre_actual = "{" + ",".join(sorted(conjunto_actual)) + "}"
            afd.agregar_estado(nombre_actual)
            if conjunto_actual & self.estados_finales:
                afd.agregar_final(nombre_actual)

            for simbolo in self.alfabeto:
                destinos = self.mover(conjunto_actual, simbolo)
                destinos = self.epsilon_closure(destinos)

                if not destinos:
                    continue

                nuevo_conjunto = frozenset(destinos)
                nombre_nuevo = "{" + ",".join(sorted(nuevo_conjunto)) + "}"

                afd.agregar_simbolo(simbolo)

                if nombre_nuevo not in afd.estados:
                    afd.agregar_estado(nombre_nuevo)

                afd.agregar_transicion(
                    nombre_actual,
                    simbolo,
                    nombre_nuevo
                )

                if nuevo_conjunto not in visitados:
                    pendientes.append(nuevo_conjunto)

        return afd