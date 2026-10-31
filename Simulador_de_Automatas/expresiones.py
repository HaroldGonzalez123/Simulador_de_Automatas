
from automata import Automata


class ExpresionRegular:
    """
    Convierte expresiones regulares en un AFN
    utilizando el algoritmo de Thompson.

    Operadores admitidos:
        |       Unión
        *       Cerradura de Kleene
        (...)   Agrupación
        AB      Concatenación implícita

    Ejemplo:
        (0|1)*01
    """

    CONCAT = "\u00b7"

    def __init__(self, expresion):
        if not isinstance(expresion, str):
            raise ValueError(
                "La expresión regular debe ser texto."
            )

        self.expresion = expresion.replace(" ", "")

        if not self.expresion:
            raise ValueError(
                "La expresión regular no puede estar vacía."
            )

        self._validar_expresion()

    # ---------------------------------------------------------
    # IDENTIFICAR OPERANDOS
    # ---------------------------------------------------------

    def _es_operando(self, simbolo):
        """
        Un operando es cualquier símbolo que no sea
        un operador ni el símbolo interno de concatenación.
        """

        return simbolo not in (
            "|",
            "*",
            "(",
            ")",
            self.CONCAT
        )

    # ---------------------------------------------------------
    # VALIDAR EXPRESIÓN
    # ---------------------------------------------------------

    def _validar_expresion(self):

        expresion = self.expresion
        balance = 0
        espera_operando = True

        for simbolo in expresion:

            if simbolo == "(":

                balance += 1
                espera_operando = True

            elif simbolo == ")":

                if espera_operando:
                    raise ValueError(
                        "Hay un paréntesis vacío "
                        "o un operador incompleto."
                    )

                balance -= 1

                if balance < 0:
                    raise ValueError(
                        "Hay paréntesis desbalanceados."
                    )

                espera_operando = False

            elif simbolo == "|":

                if espera_operando:
                    raise ValueError(
                        "La unión '|' necesita "
                        "operandos a ambos lados."
                    )

                espera_operando = True

            elif simbolo == "*":

                if espera_operando:
                    raise ValueError(
                        "El operador '*' necesita "
                        "un operando anterior."
                    )

                espera_operando = False

            elif simbolo == self.CONCAT:
                raise ValueError("Use concatenación implícita: ab, no a·b.")
            else:
                espera_operando = False

        if balance != 0:
            raise ValueError(
                "Hay paréntesis desbalanceados."
            )

        if espera_operando:
            raise ValueError(
                "La expresión termina con un operador "
                "incompleto."
            )

    # ---------------------------------------------------------
    # INSERTAR CONCATENACIONES
    # ---------------------------------------------------------

    def _agregar_concatenaciones(self):
        """
        Inserta concatenación explícita.

        Ejemplos:
            01       -> 0 · 1
            (0|1)0   -> (0|1) · 0
            0(1|0)   -> 0 · (1|0)
        """

        resultado = []
        anterior = None

        for actual in self.expresion:

            if anterior is not None:

                anterior_termina = (
                    self._es_operando(anterior)
                    or anterior == ")"
                    or anterior == "*"
                )

                actual_empieza = (
                    self._es_operando(actual)
                    or actual == "("
                )

                if anterior_termina and actual_empieza:
                    resultado.append(self.CONCAT)

            resultado.append(actual)
            anterior = actual

        return resultado

    # ---------------------------------------------------------
    # CONVERTIR A NOTACIÓN POSTFIJA
    # ---------------------------------------------------------

    def _a_postfija(self):

        precedencia = {
            "|": 1,
            self.CONCAT: 2,
            "*": 3
        }

        salida = []
        operadores = []

        for simbolo in self._agregar_concatenaciones():

            if self._es_operando(simbolo):

                salida.append(simbolo)

            elif simbolo == "(":

                operadores.append(simbolo)

            elif simbolo == ")":

                while (
                    operadores
                    and operadores[-1] != "("
                ):
                    salida.append(
                        operadores.pop()
                    )

                if not operadores:
                    raise ValueError(
                        "Paréntesis incorrectos."
                    )

                operadores.pop()

            else:

                while (
                    operadores
                    and operadores[-1] != "("
                    and precedencia[operadores[-1]]
                    >= precedencia[simbolo]
                ):
                    salida.append(
                        operadores.pop()
                    )

                operadores.append(simbolo)

        while operadores:

            operador = operadores.pop()

            if operador in ("(", ")"):
                raise ValueError(
                    "Paréntesis incorrectos."
                )

            salida.append(operador)

        return salida

    # ---------------------------------------------------------
    # CONVERTIR EXPRESIÓN REGULAR A AFN
    # ---------------------------------------------------------

    def convertir_a_afn(self):
        """
        Construye un AFN mediante el algoritmo de Thompson.
        Las transiciones epsilon se representan internamente
        con el símbolo 'e'.
        """

        postfija = self._a_postfija()

        automata = Automata()
        pila = []
        contador = 0

        def nuevo_estado():

            nonlocal contador

            estado = f"r{contador}"
            contador += 1

            automata.agregar_estado(estado)

            return estado

        def agregar_epsilon(origen, destino):

            automata.agregar_transicion(
                origen,
                "e",
                destino
            )

        for simbolo in postfija:

            # -------------------------------------------------
            # OPERANDO
            # -------------------------------------------------

            if self._es_operando(simbolo):

                inicial = nuevo_estado()
                final = nuevo_estado()

                # e y ε son épsilon, nunca letras del alfabeto.
                if simbolo in ("e", "ε"):
                    agregar_epsilon(inicial, final)
                else:
                    automata.agregar_simbolo(simbolo)
                    automata.agregar_transicion(inicial, simbolo, final)

                pila.append(
                    (inicial, final)
                )

            # -------------------------------------------------
            # CONCATENACIÓN
            # -------------------------------------------------

            elif simbolo == self.CONCAT:

                if len(pila) < 2:
                    raise ValueError(
                        "Concatenación inválida."
                    )

                fragmento_b = pila.pop()
                fragmento_a = pila.pop()

                agregar_epsilon(
                    fragmento_a[1],
                    fragmento_b[0]
                )

                pila.append(
                    (
                        fragmento_a[0],
                        fragmento_b[1]
                    )
                )

            # -------------------------------------------------
            # UNIÓN
            # -------------------------------------------------

            elif simbolo == "|":

                if len(pila) < 2:
                    raise ValueError(
                        "Unión inválida."
                    )

                fragmento_b = pila.pop()
                fragmento_a = pila.pop()

                inicial = nuevo_estado()
                final = nuevo_estado()

                agregar_epsilon(
                    inicial,
                    fragmento_a[0]
                )

                agregar_epsilon(
                    inicial,
                    fragmento_b[0]
                )

                agregar_epsilon(
                    fragmento_a[1],
                    final
                )

                agregar_epsilon(
                    fragmento_b[1],
                    final
                )

                pila.append(
                    (inicial, final)
                )

            # -------------------------------------------------
            # CERRADURA DE KLEENE
            # -------------------------------------------------

            elif simbolo == "*":

                if not pila:
                    raise ValueError(
                        "Cerradura de Kleene inválida."
                    )

                fragmento = pila.pop()

                inicial = nuevo_estado()
                final = nuevo_estado()

                # Permite entrar al fragmento
                agregar_epsilon(
                    inicial,
                    fragmento[0]
                )

                # Permite aceptar cero repeticiones
                agregar_epsilon(
                    inicial,
                    final
                )

                # Permite repetir el fragmento
                agregar_epsilon(
                    fragmento[1],
                    fragmento[0]
                )

                # Permite salir del fragmento
                agregar_epsilon(
                    fragmento[1],
                    final
                )

                pila.append(
                    (inicial, final)
                )

        # -----------------------------------------------------
        # VERIFICAR RESULTADO
        # -----------------------------------------------------

        if len(pila) != 1:
            raise ValueError(
                "No se pudo construir el AFN. "
                "Revise la expresión regular."
            )

        inicial, final = pila.pop()

        automata.definir_inicial(inicial)
        automata.agregar_final(final)

        return automata
