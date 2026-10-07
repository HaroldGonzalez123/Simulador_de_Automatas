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

    def tabla_distinguibilidad(self):

        estados = sorted(
            self.estados_alcanzables()
        )

        distinguibles = set()

        # --------------------------------------------------------
        # Marcar inicialmente los pares:
        # uno final y otro no final
        # --------------------------------------------------------

        for i in range(len(estados)):

            for j in range(i + 1, len(estados)):

                estado1 = estados[i]
                estado2 = estados[j]

                if self.son_distinguibles(
                    estado1,
                    estado2
                ):

                    distinguibles.add(
                        (estado1, estado2)
                    )

        # --------------------------------------------------------
        # Propagar distinguibilidad
        # --------------------------------------------------------

        cambio = True

        while cambio:

            cambio = False

            for i in range(len(estados)):

                for j in range(i + 1, len(estados)):

                    estado1 = estados[i]
                    estado2 = estados[j]

                    pareja = (
                        estado1,
                        estado2
                    )

                    if pareja in distinguibles:
                        continue

                    for simbolo in self.alfabeto:

                        destinos1 = self.transiciones.get(
                            (estado1, simbolo),
                            set()
                        )

                        destinos2 = self.transiciones.get(
                            (estado2, simbolo),
                            set()
                        )

                        destino1 = next(
                            iter(destinos1),
                            None
                        )

                        destino2 = next(
                            iter(destinos2),
                            None
                        )

                        if (
                            destino1 is None
                            and destino2 is None
                        ):
                            continue

                        if (
                            destino1 is None
                            or destino2 is None
                        ):

                            distinguibles.add(
                                pareja
                            )

                            cambio = True
                            break

                        siguiente = tuple(
                            sorted(
                                (
                                    destino1,
                                    destino2
                                )
                            )
                        )

                        if siguiente in distinguibles:

                            distinguibles.add(
                                pareja
                            )

                            cambio = True
                            break

        return distinguibles

    # ============================================================
    # MINIMIZAR AFD
    # ============================================================

    def minimizar_afd(self):

        pares = self.tabla_distinguibilidad()

        estados = sorted(
            self.estados
        )

        grupos = []

        # --------------------------------------------------------
        # Crear grupos de estados equivalentes
        # --------------------------------------------------------

        for estado in estados:

            grupo_encontrado = None

            for grupo in grupos:

                representante = grupo[0]

                par = tuple(
                    sorted(
                        (
                            estado,
                            representante
                        )
                    )
                )

                if par not in pares:

                    grupo_encontrado = grupo
                    break

            if grupo_encontrado:

                grupo_encontrado.append(
                    estado
                )

            else:

                grupos.append(
                    [estado]
                )

        # --------------------------------------------------------
        # Crear nuevo AFD
        # --------------------------------------------------------

        afd_minimo = Automata()

        nombres_grupos = {}

        for grupo in grupos:

            estados_limpios = []

            for estado in sorted(grupo):

                # Los estados provenientes de AFN → AFD
                # ya tienen llaves, por ejemplo:
                # {q0,q1}
                #
                # Las quitamos para evitar:
                # {{q0,q1},{q0,q2}}

                if (
                    estado.startswith("{")
                    and estado.endswith("}")
                ):

                    estado = estado[1:-1]

                estados_limpios.append(
                    estado
                )

            # Si un grupo contiene varios estados,
            # los mostramos separados por |
            #
            # Ejemplo:
            # {q0,q2 | q0,q1,q2}

            nombre = (
                "{"
                + " | ".join(estados_limpios)
                + "}"
            )

            nombres_grupos[nombre] = grupo

            afd_minimo.agregar_estado(
                nombre
            )

        # --------------------------------------------------------
        # Estado inicial
        # --------------------------------------------------------

        for nombre, grupo in nombres_grupos.items():

            if self.estado_inicial in grupo:

                afd_minimo.definir_inicial(
                    nombre
                )

        # --------------------------------------------------------
        # Estados finales
        # --------------------------------------------------------

        for nombre, grupo in nombres_grupos.items():

            if any(
                estado in self.estados_finales
                for estado in grupo
            ):

                afd_minimo.agregar_final(
                    nombre
                )

        # --------------------------------------------------------
        # Alfabeto
        # --------------------------------------------------------

        for simbolo in self.alfabeto:

            afd_minimo.agregar_simbolo(
                simbolo
            )

        # --------------------------------------------------------
        # Transiciones
        # --------------------------------------------------------

        for nombre, grupo in nombres_grupos.items():

            representante = grupo[0]

            for simbolo in self.alfabeto:

                clave = (
                    representante,
                    simbolo
                )

                if clave in self.transiciones:

                    destino = next(
                        iter(
                            self.transiciones[clave]
                        )
                    )

                    for (
                        nombre_destino,
                        grupo_destino
                    ) in nombres_grupos.items():

                        if destino in grupo_destino:

                            afd_minimo.agregar_transicion(
                                nombre,
                                simbolo,
                                nombre_destino
                            )

                            break

        return afd_minimo

    # ============================================================
    # CONVERTIR AFN → AFD
    # ============================================================

    def convertir_a_afd(self):

        if self.estado_inicial is None:

            raise ValueError(
                "Debe definir el estado inicial."
            )

        afd = Automata()

        # --------------------------------------------------------
        # Estado inicial del AFD
        # --------------------------------------------------------

        estado_inicial = frozenset(
            self.epsilon_closure(
                {self.estado_inicial}
            )
        )

        pendientes = [
            estado_inicial
        ]

        visitados = set()

        nombre_inicial = (
            "{"
            + ",".join(
                sorted(estado_inicial)
            )
            + "}"
        )

        afd.agregar_estado(
            nombre_inicial
        )

        afd.definir_inicial(
            nombre_inicial
        )

        # --------------------------------------------------------
        # Construcción por subconjuntos
        # --------------------------------------------------------

        while pendientes:

            conjunto_actual = pendientes.pop()

            if conjunto_actual in visitados:
                continue

            visitados.add(
                conjunto_actual
            )

            nombre_actual = (
                "{"
                + ",".join(
                    sorted(conjunto_actual)
                )
                + "}"
            )

            afd.agregar_estado(
                nombre_actual
            )

            # ----------------------------------------------------
            # Determinar si el conjunto contiene un estado final
            # ----------------------------------------------------

            if (
                conjunto_actual
                & self.estados_finales
            ):

                afd.agregar_final(
                    nombre_actual
                )

            # ----------------------------------------------------
            # Procesar cada símbolo
            # ----------------------------------------------------

            for simbolo in self.alfabeto:

                destinos = self.mover(
                    conjunto_actual,
                    simbolo
                )

                destinos = self.epsilon_closure(
                    destinos
                )

                if not destinos:
                    continue

                nuevo_conjunto = frozenset(
                    destinos
                )

                nombre_nuevo = (
                    "{"
                    + ",".join(
                        sorted(nuevo_conjunto)
                    )
                    + "}"
                )

                afd.agregar_simbolo(
                    simbolo
                )

                if (
                    nombre_nuevo
                    not in afd.estados
                ):

                    afd.agregar_estado(
                        nombre_nuevo
                    )

                afd.agregar_transicion(
                    nombre_actual,
                    simbolo,
                    nombre_nuevo
                )

                if (
                    nuevo_conjunto
                    not in visitados
                ):

                    pendientes.append(
                        nuevo_conjunto
                    )

        return afd