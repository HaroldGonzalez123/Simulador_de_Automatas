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

    def estados_alcanzables(self):
        if self.estado_inicial is None:
            raise ValueError("No se ha definido el estado inicial.")

        alcanzables = {self.estado_inicial}
        pendientes = [self.estado_inicial]

        while pendientes:
            estado = pendientes.pop()

            for simbolo in self.alfabeto:
                clave = (estado, simbolo)

                if clave in self.transiciones:
                    for destino in self.transiciones[clave]:
                        if destino not in alcanzables:
                            alcanzables.add(destino)
                            pendientes.append(destino)

        return alcanzables

    def son_distinguibles(self, estado1, estado2):
        if estado1 in self.estados_finales and estado2 not in self.estados_finales:
            return True

        if estado2 in self.estados_finales and estado1 not in self.estados_finales:
            return True

        return False

    def tabla_distinguibilidad(self):
        estados = sorted(self.estados_alcanzables())
        distinguibles = set()

        # Paso 1: final vs. no final
        for i in range(len(estados)):
            for j in range(i + 1, len(estados)):
                estado1 = estados[i]
                estado2 = estados[j]

                if self.son_distinguibles(estado1, estado2):
                    distinguibles.add((estado1, estado2))

        # Paso 2: propagar las distinciones
        cambio = True

        while cambio:
            cambio = False

            for i in range(len(estados)):
                for j in range(i + 1, len(estados)):
                    estado1 = estados[i]
                    estado2 = estados[j]
                    pareja = (estado1, estado2)

                    if pareja in distinguibles:
                        continue

                    for simbolo in self.alfabeto:
                        destinos1 = self.transiciones.get(
                            (estado1, simbolo), set()
                        )
                        destinos2 = self.transiciones.get(
                            (estado2, simbolo), set()
                        )

                        destino1 = next(iter(destinos1), None)
                        destino2 = next(iter(destinos2), None)

                        if destino1 is None and destino2 is None:
                            continue

                        if destino1 is None or destino2 is None:
                            distinguibles.add(pareja)
                            cambio = True
                            break

                        siguiente = tuple(sorted((destino1, destino2)))

                        if siguiente in distinguibles:
                            distinguibles.add(pareja)
                            cambio = True
                            break

        return distinguibles

    def minimizar_afd(self):
        pares = self.tabla_distinguibilidad()

        estados = sorted(self.estados)

        # Encontrar grupos de estados equivalentes
        grupos = []

        for estado in estados:
            grupo_encontrado = None

            for grupo in grupos:
                representante = grupo[0]

                par = tuple(sorted((estado, representante)))

                if par not in pares:
                    grupo_encontrado = grupo
                    break

            if grupo_encontrado:
                grupo_encontrado.append(estado)
            else:
                grupos.append([estado])

        # Crear el nuevo autómata
        afd_minimo = Automata()

        nombres_grupos = {}

        for i, grupo in enumerate(grupos):
            nombre = "{" + ",".join(sorted(grupo)) + "}"
            nombres_grupos[nombre] = grupo

            afd_minimo.agregar_estado(nombre)

        # Estado inicial
        for nombre, grupo in nombres_grupos.items():
            if self.estado_inicial in grupo:
                afd_minimo.definir_inicial(nombre)

        # Estados finales
        for nombre, grupo in nombres_grupos.items():
            if any(estado in self.estados_finales for estado in grupo):
                afd_minimo.agregar_final(nombre)

        # Alfabeto
        for simbolo in self.alfabeto:
            afd_minimo.agregar_simbolo(simbolo)

        # Transiciones
        for nombre, grupo in nombres_grupos.items():
            representante = grupo[0]

            for simbolo in self.alfabeto:
                clave = (representante, simbolo)

                if clave in self.transiciones:
                    destino = next(iter(self.transiciones[clave]))

                    for nombre_destino, grupo_destino in nombres_grupos.items():
                        if destino in grupo_destino:
                            afd_minimo.agregar_transicion(
                                nombre,
                                simbolo,
                                nombre_destino
                            )
                            break

        return afd_minimo
    
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