from automata import Automata


def mostrar_automata(automata):
    print("\n-Simulador de Automatas-")
    print("Estados:", automata.estados)
    print("Alfabeto:", automata.alfabeto)
    print("Estado inicial:", automata.estado_inicial)
    print("Estados finales:", automata.estados_finales)

    print("\nTransiciones:")

    if not automata.transiciones:
        print("No hay transiciones.")
    else:
        for (origen, simbolo), destinos in automata.transiciones.items():
            print(origen, "--", simbolo, "-->", destinos)


def crear_automata():
    automata = Automata()

    print("\n-Crea un Automata-")

    # Estados
    entrada = input("Ingrese los estados separados por una coma (ejemplo: q0,q1,q2): ")

    for estado in entrada.split(","):
        estado = estado.strip()

        if estado:
            automata.agregar_estado(estado)

    # Alfabeto
    entrada = input("Ingrese el alfabeto separado por una coma (ejemplo: 0,1): ")

    for simbolo in entrada.split(","):
        simbolo = simbolo.strip()

        if simbolo:
            automata.agregar_simbolo(simbolo)

    # Estado inicial
    inicial = input("Ingrese el estado inicial del automata: ").strip()
    automata.definir_inicial(inicial)

    # Estados finales
    entrada = input("Ingrese los estados finales separados por una coma: ")

    for estado in entrada.split(","):
        estado = estado.strip()

        if estado:
            automata.agregar_final(estado)

    # Transiciones
    print("\nIngrese las transiciones.")
    print("Para una transicion epsilon, escriba solo: e")
    print("Escriba F cuando termine.")

    while True:
        origen = input("\nEstado origen (o F): ").strip()

        if origen.upper() == "F":
            break

        simbolo = input("Simbolo (escriba 'e' para epsilon): ").strip()

        if simbolo.lower() in ("e", "epsilon"):
            simbolo = "ε"

        destino = input("Estado destino: ").strip()

        automata.agregar_transicion(origen, simbolo, destino)

    print("\nAutomata creado correctamente.")

    return automata


def main():
    automata = None

    while True:
        print("\n            ")
        print("     SIMULADOR DE AUTOMATAS")
        print("              ")
        print("1. Crear automata")
        print("2. Mostrar automata")
        print("3. Probar cadena")
        print("4. Convertir AFN a AFD")
        print("5. Minimizar AFD")
        print("6. Salir")
        print("              ")

        opcion = input("Seleccione una opcion con el numero correspondiente: ")

        try:
            if opcion == "1":
                automata = crear_automata()

            elif opcion == "2":
                if automata is None:
                    print("\nPrimero debe crear un automata.")
                else:
                    mostrar_automata(automata)

            elif opcion == "3":
                if automata is None:
                    print("\nPrimero debe crear un automata.")
                else:
                    cadena = input("Ingrese la cadena a probar: ")

                    if automata.simular(cadena):
                        print("Cadena ACEPTADA")
                    else:
                        print("Cadena RECHAZADA")

            elif opcion == "4":
                if automata is None:
                    print("\nPrimero debe crear un automata.")
                else:
                    afd = automata.convertir_a_afd()

                    print("\nAFD generado:")
                    mostrar_automata(afd)

            elif opcion == "5":
                if automata is None:
                    print("\nPrimero debe crear un automata.")
                else:
                    afd_minimo = automata.minimizar_afd()

                    print("\nAFD minimizado:")
                    mostrar_automata(afd_minimo)

            elif opcion == "6":
                print("\nPrograma finalizado.")
                break

            else:
                print("\nOpcion no valida.")

        except ValueError as error:
            print("\nERROR:", error)


if __name__ == "__main__":
    main()