class Automata:

    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.estado_inicial = None
        self.estados_finales = set()
        self.transiciones = {}

    # ============================================================
    # ESTADOS
    # ============================================================

    def agregar_estado(self, estado):
        self.estados.add(estado)

    # ============================================================
    # ALFABETO
    # ============================================================

    def agregar_simbolo(self, simbolo):
        if not isinstance(simbolo, str) or len(simbolo) != 1:
            raise ValueError("Ingrese solamente un símbolo.")
        if simbolo in ("e", "ε"):
            raise ValueError("e y ε están reservados para épsilon.")
        self.alfabeto.add(simbolo)

    # ============================================================
    # ESTADO INICIAL
    # ============================================================

    def definir_inicial(self, estado):

        if estado not in self.estados:
            raise ValueError(
                "El estado inicial debe existir."
            )

        self.estado_inicial = estado

    # ============================================================
    # ESTADOS FINALES
    # ============================================================

    def agregar_final(self, estado):

        if estado not in self.estados:
            raise ValueError(
                "El estado final debe existir."
            )

        self.estados_finales.add(estado)

    # ============================================================
    # TRANSICIONES
    # ============================================================

    def agregar_transicion(self, origen, simbolo, destino):
        if simbolo == "ε":
            simbolo = "e"


        if origen not in self.estados:
            raise ValueError(
                "El estado de origen no existe."
            )

        if destino not in self.estados:
            raise ValueError(
                "El estado de destino no existe."
            )

        # "e" representa epsilon internamente
        if simbolo != "e" and simbolo not in self.alfabeto:
            raise ValueError(
                "El símbolo no pertenece al alfabeto."
            )

        clave = (origen, simbolo)

        self.transiciones.setdefault(
            clave,
            set()
        ).add(destino)

    # ============================================================
    # CERRADURA EPSILON
    # ============================================================

    def epsilon_closure(self, estados):

        clausura = set(estados)
        pendientes = list(estados)

        while pendientes:

            estado = pendientes.pop()

            clave = (estado, "e")

            if clave in self.transiciones:

                for destino in self.transiciones[clave]:

                    if destino not in clausura:

                        clausura.add(destino)
                        pendientes.append(destino)

        return clausura

    # ============================================================
    # MOVER
    # ============================================================

    def mover(self, estados, simbolo):

        destinos = set()

        for estado in estados:

            clave = (estado, simbolo)

            if clave in self.transiciones:

                destinos.update(
                    self.transiciones[clave]
                )

        return destinos

    # ============================================================
    # SIMULACIÓN
    # ============================================================

    def simular(self, cadena):

        if self.estado_inicial is None:

            raise ValueError(
                "No se ha definido el estado inicial."
            )

        estados_actuales = self.epsilon_closure(
            {self.estado_inicial}
        )

        for simbolo in cadena:

            if simbolo not in self.alfabeto:
                return False

            estados_actuales = self.mover(
                estados_actuales,
                simbolo
            )

            if not estados_actuales:
                return False

            estados_actuales = self.epsilon_closure(
                estados_actuales
            )

        return bool(
            estados_actuales &
            self.estados_finales
        )

    # ============================================================
    # ESTADOS ALCANZABLES
    # ============================================================

    def estados_alcanzables(self):

        if self.estado_inicial is None:
            return set()

        alcanzables = {
            self.estado_inicial
        }

        pendientes = [
            self.estado_inicial
        ]

        while pendientes:

            estado_actual = pendientes.pop()

            for (origen, simbolo), destinos in self.transiciones.items():

                if origen != estado_actual:
                    continue

                for destino in destinos:

                    if destino not in alcanzables:

                        alcanzables.add(destino)
                        pendientes.append(destino)

        return alcanzables

    # ============================================================
    # ESTADOS DISTINGUIBLES
    # ============================================================

    def son_distinguibles(self, estado1, estado2):

        if (
            estado1 in self.estados_finales
            and estado2 not in self.estados_finales
        ):
            return True

        if (
            estado2 in self.estados_finales
            and estado1 not in self.estados_finales
        ):
            return True

        return False

    # ============================================================
    # TABLA DE DISTINGUIBILIDAD
    # ============================================================

    def es_determinista(self):
        return all(simbolo != "e" and len(destinos) == 1
                   for (_, simbolo), destinos in self.transiciones.items())

    def _afd_completo(self):
        """Copia determinista, alcanzable y total; incluye el conjunto vacío."""
        return self.convertir_a_afd()

    def tabla_distinguibilidad(self):
        """Pares distinguibles del AFD original, considerando un pozo implícito."""
        if not self.es_determinista():
            raise ValueError("Convierta el AFN a AFD antes de crear esta tabla.")
        if self.estado_inicial is None:
            raise ValueError("Debe definir el estado inicial.")
        estados = sorted(self.estados_alcanzables())
        pozo = object()
        todos = estados + [pozo]
        def destino(q, simbolo):
            return next(iter(self.transiciones.get((q, simbolo), ())), pozo)
        pares = set()
        for i, a in enumerate(todos):
            for b in todos[i + 1:]:
                if (a in self.estados_finales) != (b in self.estados_finales):
                    pares.add(frozenset((a, b)))
        cambio = True
        while cambio:
            cambio = False
            for i, a in enumerate(todos):
                for b in todos[i + 1:]:
                    par = frozenset((a, b))
                    if par not in pares and any(
                        frozenset((destino(a, s), destino(b, s))) in pares
                        for s in self.alfabeto
                    ):
                        pares.add(par)
                        cambio = True
        return {(a, b) for i, a in enumerate(estados) for b in estados[i + 1:]
                if frozenset((a, b)) in pares}

    def minimizar_afd(self):
        """Determiniza y completa antes de minimizar por refinamiento de particiones."""
        afd = self._afd_completo()
        grupos = [g for g in (afd.estados_finales,
                              afd.estados - afd.estados_finales) if g]
        simbolos = sorted(afd.alfabeto)
        while True:
            indice = {q: i for i, grupo in enumerate(grupos) for q in grupo}
            nuevos = []
            for grupo in grupos:
                bloques = {}
                for q in sorted(grupo):
                    firma = tuple(indice[next(iter(afd.transiciones[(q, s)]))]
                                  for s in simbolos)
                    bloques.setdefault(firma, set()).add(q)
                nuevos.extend(bloques.values())
            if len(nuevos) == len(grupos):
                grupos = nuevos
                break
            grupos = nuevos
        minimo = Automata()
        nombres = {q: f"M{i}" for i, grupo in enumerate(grupos) for q in grupo}
        for nombre in nombres.values():
            minimo.agregar_estado(nombre)
        for simbolo in simbolos:
            minimo.agregar_simbolo(simbolo)
        minimo.definir_inicial(nombres[afd.estado_inicial])
        for q in afd.estados_finales:
            minimo.agregar_final(nombres[q])
        for grupo in grupos:
            q = min(grupo)
            for simbolo in simbolos:
                destino = next(iter(afd.transiciones[(q, simbolo)]))
                minimo.agregar_transicion(nombres[q], simbolo, nombres[destino])
        return minimo

    def convertir_a_afd(self):
        """Construcción por subconjuntos con nombres únicos y estado pozo."""
        if self.estado_inicial is None:
            raise ValueError("Debe definir el estado inicial.")
        afd = Automata()
        for simbolo in self.alfabeto:
            afd.agregar_simbolo(simbolo)
        inicial = frozenset(self.epsilon_closure({self.estado_inicial}))
        nombres = {inicial: "D0"}
        pendientes = [inicial]
        afd.agregar_estado("D0")
        afd.definir_inicial("D0")
        while pendientes:
            actual = pendientes.pop(0)
            nombre = nombres[actual]
            if actual & self.estados_finales:
                afd.agregar_final(nombre)
            for simbolo in sorted(self.alfabeto):
                destino = frozenset(self.epsilon_closure(self.mover(actual, simbolo)))
                if destino not in nombres:
                    nombres[destino] = f"D{len(nombres)}"
                    afd.agregar_estado(nombres[destino])
                    pendientes.append(destino)
                afd.agregar_transicion(nombre, simbolo, nombres[destino])
        return afd
