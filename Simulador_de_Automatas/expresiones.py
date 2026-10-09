from automata import Automata


class ExpresionRegular:

    # ============================================================
    # CONSTRUCTOR
    # ============================================================

    def __init__(self, expresion):
        self.expresion = expresion.replace(" ", "")

    # ============================================================
    # DETERMINAR SI ES UN OPERANDO
    # ============================================================

    @staticmethod
    def es_operando(caracter):

        return caracter not in {
            "|",
            ".",
            "*",
            "(",
            ")"
        }

    # ============================================================
    # AGREGAR CONCATENACIÓN EXPLÍCITA
    # ============================================================

    def agregar_concatenacion(self):

        resultado = ""

        for i, actual in enumerate(self.expresion):

            resultado += actual

            if i + 1 >= len(self.expresion):
                continue

            siguiente = self.expresion[i + 1]

            izquierda_valida = (
                self.es_operando(actual)
                or actual == ")"
                or actual == "*"
            )

            derecha_valida = (
                self.es_operando(siguiente)
                or siguiente == "("
            )

            if izquierda_valida and derecha_valida:
                resultado += "."

        return resultado

    # ============================================================
    # PRECEDENCIA DE OPERADORES
    # ============================================================

    @staticmethod
    def precedencia(operador):

        if operador == "|":
            return 1

        if operador == ".":
            return 2

        if operador == "*":
            return 3

        return 0

    # ============================================================
    # CONVERTIR INFIX → POSTFIX
    # ============================================================

    def a_postfija(self):

        expresion = self.agregar_concatenacion()

        salida = []
        operadores = []

        for caracter in expresion:

            # ----------------------------------------------------
            # OPERANDO
            # ----------------------------------------------------

            if self.es_operando(caracter):

                salida.append(caracter)

            # ----------------------------------------------------
            # PARÉNTESIS IZQUIERDO
            # ----------------------------------------------------

            elif caracter == "(":

                operadores.append(caracter)

            # ----------------------------------------------------
            # PARÉNTESIS DERECHO
            # ----------------------------------------------------

            elif caracter == ")":

                encontrado_parentesis = False

                while operadores:

                    operador = operadores.pop()

                    if operador == "(":

                        encontrado_parentesis = True
                        break

                    salida.append(operador)

                if not encontrado_parentesis:

                    raise ValueError(
                        "Paréntesis desbalanceados."
                    )

            # ----------------------------------------------------
            # OPERADORES
            # ----------------------------------------------------

            elif caracter in {"|", ".", "*"}:

                # La estrella de Kleene es unaria
                if caracter == "*":

                    if not salida:

                        raise ValueError(
                            "El operador * no tiene un operando."
                        )

                    salida.append("*")

                    continue

                while (
                    operadores
                    and operadores[-1] != "("
                    and self.precedencia(
                        operadores[-1]
                    ) >= self.precedencia(caracter)
                ):

                    salida.append(
                        operadores.pop()
                    )

                operadores.append(caracter)

            else:

                raise ValueError(
                    f"Símbolo no reconocido: {caracter}"
                )

        # --------------------------------------------------------
        # VACIAR OPERADORES
        # --------------------------------------------------------

        while operadores:

            operador = operadores.pop()

            if operador in {"(", ")"}:

                raise ValueError(
                    "Paréntesis desbalanceados."
                )

            salida.append(operador)

        return salida

    # ============================================================
    # CONSTRUCCIÓN DE THOMPSON
    # ============================================================

    def convertir_a_afn(self):

        postfija = self.a_postfija()

        if not postfija:

            raise ValueError(
                "La expresión regular está vacía."
            )

        automata = Automata()

        contador_estado = 0

        pila = []

        # --------------------------------------------------------
        # CREAR NUEVO ESTADO
        # --------------------------------------------------------

        def nuevo_estado():

            nonlocal contador_estado

            estado = f"q{contador_estado}"

            contador_estado += 1

            automata.agregar_estado(
                estado
            )

            return estado

        # --------------------------------------------------------
        # PROCESAR EXPRESIÓN POSTFIJA
        # --------------------------------------------------------

        for token in postfija:

            # ====================================================
            # OPERANDO
            # ====================================================

            if self.es_operando(token):

                inicio = nuevo_estado()
                fin = nuevo_estado()

                if token == "ε":

                    automata.agregar_transicion(
                        inicio,
                        "e",
                        fin
                    )

                else:

                    automata.agregar_simbolo(
                        token
                    )

                    automata.agregar_transicion(
                        inicio,
                        token,
                        fin
                    )

                pila.append(
                    (inicio, fin)
                )

            # ====================================================
            # CONCATENACIÓN
            # ====================================================

            elif token == ".":

                if len(pila) < 2:

                    raise ValueError(
                        "Error en la concatenación."
                    )

                segundo = pila.pop()
                primero = pila.pop()

                automata.agregar_transicion(
                    primero[1],
                    "e",
                    segundo[0]
                )

                pila.append(
                    (
                        primero[0],
                        segundo[1]
                    )
                )

            # ====================================================
            # UNIÓN
            # ====================================================

            elif token == "|":

                if len(pila) < 2:

                    raise ValueError(
                        "Error en la unión."
                    )

                segundo = pila.pop()
                primero = pila.pop()

                inicio = nuevo_estado()
                fin = nuevo_estado()

                # Inicio → primero
                automata.agregar_transicion(
                    inicio,
                    "e",
                    primero[0]
                )

                # Inicio → segundo
                automata.agregar_transicion(
                    inicio,
                    "e",
                    segundo[0]
                )

                # Primero → fin
                automata.agregar_transicion(
                    primero[1],
                    "e",
                    fin
                )

                # Segundo → fin
                automata.agregar_transicion(
                    segundo[1],
                    "e",
                    fin
                )

                pila.append(
                    (
                        inicio,
                        fin
                    )
                )

            # ====================================================
            # ESTRELLA DE KLEENE
            # ====================================================

            elif token == "*":

                if len(pila) < 1:

                    raise ValueError(
                        "Error en la estrella de Kleene."
                    )

                fragmento = pila.pop()

                inicio = nuevo_estado()
                fin = nuevo_estado()

                # Inicio → fragmento
                automata.agregar_transicion(
                    inicio,
                    "e",
                    fragmento[0]
                )

                # Inicio → fin
                automata.agregar_transicion(
                    inicio,
                    "e",
                    fin
                )

                # Fragmento → fragmento
                automata.agregar_transicion(
                    fragmento[1],
                    "e",
                    fragmento[0]
                )

                # Fragmento → fin
                automata.agregar_transicion(
                    fragmento[1],
                    "e",
                    fin
                )

                pila.append(
                    (
                        inicio,
                        fin
                    )
                )

        # ========================================================
        # COMPROBAR RESULTADO
        # ========================================================

        if len(pila) != 1:

            raise ValueError(
                "La expresión regular no es válida."
            )

        inicio, fin = pila.pop()

        automata.definir_inicial(
            inicio
        )

        automata.agregar_final(
            fin
        )

        return automata