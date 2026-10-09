import tkinter as tk
from tkinter import messagebox
import textwrap

from automata import Automata
from expresiones import ExpresionRegular


def iniciar_interfaz():

    automata = Automata()
    posiciones = {}
    modo_actual = "AFN / AFD"

    ventana = tk.Tk()
    ventana.title("Simulador de Autómatas")
    ventana.geometry("1100x700")
    ventana.minsize(950, 600)

    # ============================================================
    # FUNCIONES GENERALES
    # ============================================================

    def mostrar_mensaje(texto):
        etiqueta_mensaje.config(text=texto)

    def normalizar_simbolo(simbolo):
        if simbolo == "ε":
            return "e"
        return simbolo

    def simbolo_visual(simbolo):
        if simbolo == "e":
            return "ε"
        return simbolo

    # ============================================================
    # CENTRAR TÍTULO
    # ============================================================

    def centrar_titulo(event=None):

        if not canvas.find_withtag("titulo"):
            return

        ancho = canvas.winfo_width()

        if ancho <= 1:
            return

        canvas.coords(
            "titulo",
            ancho / 2,
            30
        )

    # ============================================================
    # FORMATO VISUAL DE ESTADOS
    # ============================================================

    def nombre_visual_estado(estado):

        if len(estado) <= 12:
            return estado

        return textwrap.fill(
            estado,
            width=13,
            break_long_words=False,
            break_on_hyphens=False
        )

    # ============================================================
    # ORGANIZAR POSICIONES
    # ============================================================

    def organizar_posiciones():

        posiciones.clear()

        estados = sorted(
            automata.estados
        )

        cantidad = len(estados)

        if cantidad <= 4:

            columnas = 2

            for i, estado in enumerate(estados):

                columna = i % columnas
                fila = i // columnas

                x = 230 + columna * 430
                y = 180 + fila * 230

                posiciones[estado] = (
                    x,
                    y
                )

        else:

            columnas = 3

            for i, estado in enumerate(estados):

                columna = i % columnas
                fila = i // columnas

                x = 180 + columna * 330
                y = 160 + fila * 190

                posiciones[estado] = (
                    x,
                    y
                )

    # ============================================================
    # TAMAÑO DE LOS ESTADOS
    # ============================================================

    def tamaño_estado(estado):

        nombre = nombre_visual_estado(
            estado
        )

        cantidad_lineas = (
            nombre.count("\n") + 1
        )

        if len(estado) > 20:

            ancho = 80

            alto = max(
                55,
                25 * cantidad_lineas
            )

        elif len(estado) > 12:

            ancho = 65

            alto = max(
                50,
                23 * cantidad_lineas
            )

        else:

            ancho = 45
            alto = 45

        return ancho, alto

    # ============================================================
    # DIBUJAR AUTOMATA
    # ============================================================

    def dibujar_automata():

        canvas.delete("all")

        ancho_canvas = canvas.winfo_width()

        if ancho_canvas <= 1:
            ancho_canvas = 700

        # --------------------------------------------------------
        # TÍTULO
        # --------------------------------------------------------

        canvas.create_text(
            ancho_canvas / 2,
            30,
            text=f"Visualización: {modo_actual}",
            font=("Arial", 16, "bold"),
            anchor="center",
            tags="titulo"
        )

        # --------------------------------------------------------
        # AGRUPAR BUCLES
        # --------------------------------------------------------

        bucles = {}

        for (
            origen,
            simbolo
        ), destinos in automata.transiciones.items():

            if origen not in posiciones:
                continue

            if origen in destinos:

                if origen not in bucles:
                    bucles[origen] = []

                bucles[origen].append(
                    simbolo_visual(simbolo)
                )

        # --------------------------------------------------------
        # AGRUPAR TRANSICIONES NORMALES
        # --------------------------------------------------------

        transiciones_agrupadas = {}

        for (
            origen,
            simbolo
        ), destinos in automata.transiciones.items():

            if origen not in posiciones:
                continue

            for destino in destinos:

                if destino not in posiciones:
                    continue

                if origen == destino:
                    continue

                clave = (
                    origen,
                    destino
                )

                if clave not in transiciones_agrupadas:

                    transiciones_agrupadas[
                        clave
                    ] = []

                simbolo_actual = simbolo_visual(
                    simbolo
                )

                if simbolo_actual not in transiciones_agrupadas[
                    clave
                ]:

                    transiciones_agrupadas[
                        clave
                    ].append(
                        simbolo_actual
                    )

        # --------------------------------------------------------
        # DIBUJAR TRANSICIONES
        # --------------------------------------------------------

        for (
            origen,
            destino
        ), simbolos in transiciones_agrupadas.items():

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]

            # ----------------------------------------------------
            # COMPROBAR TRANSICIÓN INVERSA
            # ----------------------------------------------------

            existe_inversa = (
                destino,
                origen
            ) in transiciones_agrupadas

            texto = ", ".join(
                simbolos
            )

            if existe_inversa:

                # Vector entre los estados
                dx = x2 - x1
                dy = y2 - y1

                distancia = max(
                    (dx ** 2 + dy ** 2) ** 0.5,
                    1
                )

                # Separación de las dos direcciones
                desplazamiento = 45

                offset_x = (
                    -dy / distancia
                ) * desplazamiento

                offset_y = (
                    dx / distancia
                ) * desplazamiento

                # Punto central desplazado
                mx = (
                    (x1 + x2) / 2
                    + offset_x
                )

                my = (
                    (y1 + y2) / 2
                    + offset_y
                )

                # ------------------------------------------------
                # CURVA
                # ------------------------------------------------

                canvas.create_line(
                    x1,
                    y1,
                    mx,
                    my,
                    x2,
                    y2,
                    smooth=True,
                    splinesteps=20,
                    arrow=tk.LAST,
                    width=2
                )

                # ------------------------------------------------
                # TEXTO
                # ------------------------------------------------

                canvas.create_text(
                    mx,
                    my - 12,
                    text=texto,
                    font=(
                        "Arial",
                        11,
                        "bold"
                    )
                )

            else:

                # ------------------------------------------------
                # TRANSICIÓN NORMAL
                # ------------------------------------------------

                canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    arrow=tk.LAST,
                    width=2
                )

                mx = (
                    x1 + x2
                ) / 2

                my = (
                    y1 + y2
                ) / 2

                canvas.create_text(
                    mx,
                    my - 15,
                    text=texto,
                    font=(
                        "Arial",
                        11,
                        "bold"
                    ),
                    fill="black"
                )

        # --------------------------------------------------------
        # DIBUJAR BUCLES
        # --------------------------------------------------------

        for estado, simbolos in bucles.items():

            x, y = posiciones[estado]

            ancho, alto = tamaño_estado(
                estado
            )

            canvas.create_oval(
                x - ancho / 2,
                y - alto / 2 - 45,
                x + ancho / 2,
                y + alto / 2 - 5,
                outline="black",
                width=2
            )

            texto_bucle = ", ".join(
                simbolos
            )

            canvas.create_text(
                x,
                y - alto / 2 - 55,
                text=texto_bucle,
                font=(
                    "Arial",
                    11,
                    "bold"
                )
            )

        # --------------------------------------------------------
        # DIBUJAR ESTADOS
        # --------------------------------------------------------

        for estado, (
            x,
            y
        ) in posiciones.items():

            ancho, alto = tamaño_estado(
                estado
            )

            # ----------------------------------------------------
            # FLECHA DEL ESTADO INICIAL
            # ----------------------------------------------------

            if estado == automata.estado_inicial:

                canvas.create_line(
                    x - ancho - 45,
                    y,
                    x - ancho,
                    y,
                    arrow=tk.LAST,
                    width=2
                )

            # ----------------------------------------------------
            # CÍRCULO DEL ESTADO
            # ----------------------------------------------------

            canvas.create_oval(
                x - ancho,
                y - alto,
                x + ancho,
                y + alto,
                fill="white",
                outline="black",
                width=2
            )

            # ----------------------------------------------------
            # ESTADO FINAL
            # ----------------------------------------------------

            if estado in automata.estados_finales:

                canvas.create_oval(
                    x - ancho + 7,
                    y - alto + 7,
                    x + ancho - 7,
                    y + alto - 7,
                    outline="black",
                    width=2
                )

            # ----------------------------------------------------
            # NOMBRE DEL ESTADO
            # ----------------------------------------------------

            tamaño_fuente = 9

            if len(estado) <= 12:
                tamaño_fuente = 10

            canvas.create_text(
                x,
                y,
                text=nombre_visual_estado(
                    estado
                ),
                font=(
                    "Arial",
                    tamaño_fuente,
                    "bold"
                ),
                justify="center"
            )

        # --------------------------------------------------------
        # ACTUALIZAR ÁREA DESPLAZABLE
        # --------------------------------------------------------

        actualizar_scroll_derecho()

    # ============================================================
    # AGREGAR ESTADO
    # ============================================================

    def agregar_estado():

        estado = entrada_estado.get().strip()

        if not estado:

            messagebox.showerror(
                "Error",
                "Ingrese el nombre del estado."
            )

            return

        if estado in automata.estados:

            messagebox.showerror(
                "Error",
                "Ese estado ya existe."
            )

            return

        automata.agregar_estado(
            estado
        )

        cantidad = len(posiciones)

        columnas = 4

        x = (
            120
            + (cantidad % columnas) * 180
        )

        y = (
            150
            + (cantidad // columnas) * 150
        )

        posiciones[estado] = (
            x,
            y
        )

        entrada_estado.delete(
            0,
            tk.END
        )

        mostrar_mensaje(
            f"Estado '{estado}' agregado correctamente."
        )

        dibujar_automata()

    # ============================================================
    # AGREGAR SÍMBOLO
    # ============================================================

    def agregar_simbolo():

        simbolo = entrada_simbolo.get().strip()

        if not simbolo:

            messagebox.showerror(
                "Error",
                "Ingrese un símbolo."
            )

            return

        simbolo = normalizar_simbolo(
            simbolo
        )

        if simbolo == "e":

            messagebox.showerror(
                "Error",
                "La letra 'e' se utiliza para representar ε."
            )

            return

        if len(simbolo) != 1:

            messagebox.showerror(
                "Error",
                "Ingrese solamente un símbolo."
            )

            return

        if simbolo in automata.alfabeto:

            messagebox.showerror(
                "Error",
                "Ese símbolo ya existe."
            )

            return

        automata.agregar_simbolo(
            simbolo
        )

        entrada_simbolo.delete(
            0,
            tk.END
        )

        mostrar_mensaje(
            f"Símbolo '{simbolo}' agregado correctamente."
        )

    # ============================================================
    # DEFINIR ESTADO INICIAL
    # ============================================================

    def definir_inicial():

        estado = entrada_inicial.get().strip()

        if not estado:

            messagebox.showerror(
                "Error",
                "Ingrese un estado."
            )

            return

        try:

            automata.definir_inicial(
                estado
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        entrada_inicial.delete(
            0,
            tk.END
        )

        mostrar_mensaje(
            f"Estado inicial: {estado}"
        )

        dibujar_automata()

    # ============================================================
    # DEFINIR ESTADO FINAL
    # ============================================================

    def definir_final():

        estado = entrada_final.get().strip()

        if not estado:

            messagebox.showerror(
                "Error",
                "Ingrese un estado."
            )

            return

        try:

            automata.agregar_final(
                estado
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        entrada_final.delete(
            0,
            tk.END
        )

        mostrar_mensaje(
            f"Estado final: {estado}"
        )

        dibujar_automata()

    # ============================================================
    # AGREGAR TRANSICIÓN
    # ============================================================

    def agregar_transicion():

        origen = entrada_origen.get().strip()

        simbolo = (
            entrada_transicion
            .get()
            .strip()
        )

        destino = entrada_destino.get().strip()

        if not origen or not simbolo or not destino:

            messagebox.showerror(
                "Error",
                "Complete todos los campos de la transición."
            )

            return

        if origen not in automata.estados:

            messagebox.showerror(
                "Error",
                f"El estado '{origen}' no existe."
            )

            return

        if destino not in automata.estados:

            messagebox.showerror(
                "Error",
                f"El estado '{destino}' no existe."
            )

            return

        simbolo = normalizar_simbolo(
            simbolo
        )

        try:

            automata.agregar_transicion(
                origen,
                simbolo,
                destino
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        entrada_origen.delete(
            0,
            tk.END
        )

        entrada_transicion.delete(
            0,
            tk.END
        )

        entrada_destino.delete(
            0,
            tk.END
        )

        mostrar_mensaje(
            f"Transición agregada: "
            f"{origen} --{simbolo_visual(simbolo)}--> {destino}"
        )

        dibujar_automata()

    # ============================================================
    # SIMULAR CADENA
    # ============================================================

    def simular_cadena():

        cadena = entrada_cadena.get()

        try:

            resultado = automata.simular(
                cadena
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        if resultado:

            etiqueta_resultado.config(
                text="✓ CADENA ACEPTADA"
            )

        else:

            etiqueta_resultado.config(
                text="✗ CADENA RECHAZADA"
            )

        mostrar_mensaje(
            f"Simulación realizada para: '{cadena}'"
        )

    # ============================================================
    # GENERAR AFN DESDE EXPRESIÓN REGULAR
    # ============================================================

    def generar_afn_regex():

        nonlocal automata
        nonlocal posiciones
        nonlocal modo_actual

        expresion = entrada_regex.get().strip()

        if not expresion:

            messagebox.showerror(
                "Expresión regular",
                "Ingrese una expresión regular."
            )

            return

        try:

            expresion_regular = (
                ExpresionRegular(
                    expresion
                )
            )

            nuevo_automata = (
                expresion_regular
                .convertir_a_afn()
            )

        except ValueError as error:

            messagebox.showerror(
                "Expresión regular inválida",
                str(error)
            )

            return

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo generar el AFN:\n{error}"
            )

            return

        automata = nuevo_automata

        modo_actual = (
            "AFN GENERADO DESDE REGEX"
        )

        organizar_posiciones()

        etiqueta_resultado.config(
            text=""
        )

        mostrar_mensaje(
            f"AFN generado correctamente desde: {expresion}"
        )

        dibujar_automata()

    # ============================================================
    # CONVERTIR AFN → AFD
    # ============================================================

    def convertir_a_afd():

        nonlocal automata
        nonlocal posiciones
        nonlocal modo_actual

        try:

            afd = (
                automata
                .convertir_a_afd()
            )

        except ValueError as error:

            messagebox.showerror(
                "Error de conversión",
                str(error)
            )

            return

        automata = afd

        modo_actual = (
            "AFD CONVERTIDO"
        )

        organizar_posiciones()

        etiqueta_resultado.config(
            text=""
        )

        mostrar_mensaje(
            "AFN convertido a AFD correctamente."
        )

        dibujar_automata()

    # ============================================================
    # MINIMIZAR AFD
    # ============================================================

    def minimizar_afd():

        nonlocal automata
        nonlocal posiciones
        nonlocal modo_actual

        try:

            afd_minimo = (
                automata
                .minimizar_afd()
            )

        except Exception as error:

            messagebox.showerror(
                "Error de minimización",
                str(error)
            )

            return

        automata = afd_minimo

        modo_actual = (
            "AFD MINIMIZADO"
        )

        organizar_posiciones()

        etiqueta_resultado.config(
            text=""
        )

        mostrar_mensaje(
            "AFD minimizado correctamente."
        )

        dibujar_automata()

    # ============================================================
    # LIMPIAR AUTÓMATA
    # ============================================================

    def limpiar_automata():

        nonlocal automata
        nonlocal posiciones
        nonlocal modo_actual

        respuesta = messagebox.askyesno(
            "Limpiar",
            "¿Desea eliminar el autómata actual?"
        )

        if not respuesta:
            return

        automata = Automata()

        posiciones.clear()

        modo_actual = "AFN / AFD"

        entrada_regex.delete(
            0,
            tk.END
        )

        entrada_cadena.delete(
            0,
            tk.END
        )

        etiqueta_resultado.config(
            text=""
        )

        mostrar_mensaje(
            "Autómata limpiado."
        )

        dibujar_automata()

    # ============================================================
    # PANEL IZQUIERDO
    # ============================================================

    marco_panel = tk.Frame(
        ventana,
        width=350,
        bg="#eeeeee"
    )

    marco_panel.pack(
        side=tk.LEFT,
        fill=tk.Y
    )

    marco_panel.pack_propagate(False)

    canvas_panel = tk.Canvas(
        marco_panel,
        bg="#eeeeee",
        highlightthickness=0
    )

    canvas_panel.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True
    )

    scrollbar = tk.Scrollbar(
        marco_panel,
        orient=tk.VERTICAL,
        command=canvas_panel.yview
    )

    scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    canvas_panel.configure(
        yscrollcommand=scrollbar.set
    )

    panel = tk.Frame(
        canvas_panel,
        bg="#eeeeee"
    )

    ventana_panel = canvas_panel.create_window(
        (0, 0),
        window=panel,
        anchor="nw"
    )

    def actualizar_scroll(event=None):

        canvas_panel.configure(
            scrollregion=canvas_panel.bbox(
                "all"
            )
        )

    panel.bind(
        "<Configure>",
        actualizar_scroll
    )

    def ajustar_ancho_panel(event):

        canvas_panel.itemconfig(
            ventana_panel,
            width=event.width
        )

    canvas_panel.bind(
        "<Configure>",
        ajustar_ancho_panel
    )

    # ============================================================
    # DESPLAZAMIENTO CON RUEDA DEL MOUSE
    # ============================================================

    def desplazamiento_mouse(event):

        widget = ventana.winfo_containing(
            event.x_root,
            event.y_root
        )

        while widget is not None:

            if widget == canvas_panel:

                canvas_panel.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

                return "break"

            if widget == canvas:

                canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

                return "break"

            widget = widget.master

        return None

    ventana.bind_all(
        "<MouseWheel>",
        desplazamiento_mouse
    )

    # ============================================================
    # TÍTULO DEL PANEL
    # ============================================================

    titulo = tk.Label(
        panel,
        text="SIMULADOR DE AUTÓMATAS",
        font=("Arial", 14, "bold"),
        bg="#eeeeee",
        anchor="center",
        justify="center",
        wraplength=300
    )

    titulo.pack(
        fill=tk.X,
        pady=20,
        padx=10
    )

    # ============================================================
    # EXPRESIÓN REGULAR
    # ============================================================

    tk.Label(
        panel,
        text="Expresión regular",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(5, 0)
    )

    entrada_regex = tk.Entry(
        panel,
        width=25
    )

    entrada_regex.pack(
        pady=5
    )

    tk.Label(
        panel,
        text="Ejemplo: (0|1)*01",
        font=("Arial", 9),
        bg="#eeeeee"
    ).pack()

    tk.Button(
        panel,
        text="Generar AFN desde Regex",
        width=22,
        command=generar_afn_regex
    ).pack(
        pady=5
    )

    # ============================================================
    # ESTADOS
    # ============================================================

    tk.Label(
        panel,
        text="Agregar estado",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    entrada_estado = tk.Entry(
        panel,
        width=25
    )

    entrada_estado.pack(
        pady=5
    )

    tk.Button(
        panel,
        text="Agregar estado",
        width=22,
        command=agregar_estado
    ).pack(
        pady=3
    )

    # ============================================================
    # ESTADO INICIAL
    # ============================================================

    tk.Label(
        panel,
        text="Estado inicial",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    entrada_inicial = tk.Entry(
        panel,
        width=25
    )

    entrada_inicial.pack(
        pady=5
    )

    tk.Button(
        panel,
        text="Definir inicial",
        width=22,
        command=definir_inicial
    ).pack(
        pady=3
    )

    # ============================================================
    # ESTADO FINAL
    # ============================================================

    tk.Label(
        panel,
        text="Estado final",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    entrada_final = tk.Entry(
        panel,
        width=25
    )

    entrada_final.pack(
        pady=5
    )

    tk.Button(
        panel,
        text="Agregar final",
        width=22,
        command=definir_final
    ).pack(
        pady=3
    )

    # ============================================================
    # ALFABETO
    # ============================================================

    tk.Label(
        panel,
        text="Símbolo del alfabeto",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    entrada_simbolo = tk.Entry(
        panel,
        width=25
    )

    entrada_simbolo.pack(
        pady=5
    )

    tk.Button(
        panel,
        text="Agregar símbolo",
        width=22,
        command=agregar_simbolo
    ).pack(
        pady=3
    )

    # ============================================================
    # TRANSICIÓN
    # ============================================================

    tk.Label(
        panel,
        text="Transición",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    entrada_origen = tk.Entry(
        panel,
        width=25
    )

    entrada_origen.pack(
        pady=3
    )

    entrada_transicion = tk.Entry(
        panel,
        width=25
    )

    entrada_transicion.pack(
        pady=3
    )

    entrada_destino = tk.Entry(
        panel,
        width=25
    )

    entrada_destino.pack(
        pady=3
    )

    tk.Label(
        panel,
        text="Origen / Símbolo / Destino",
        font=("Arial", 9),
        bg="#eeeeee"
    ).pack()

    tk.Button(
        panel,
        text="Agregar transición",
        width=22,
        command=agregar_transicion
    ).pack(
        pady=5
    )

    # ============================================================
    # SIMULAR CADENA
    # ============================================================

    tk.Label(
        panel,
        text="Simular cadena",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    entrada_cadena = tk.Entry(
        panel,
        width=25
    )

    entrada_cadena.pack(
        pady=5
    )

    tk.Button(
        panel,
        text="Simular",
        width=22,
        command=simular_cadena
    ).pack(
        pady=3
    )

    # ============================================================
    # TRANSFORMACIONES
    # ============================================================

    tk.Label(
        panel,
        text="Transformaciones",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack(
        pady=(15, 0)
    )

    tk.Button(
        panel,
        text="Convertir AFN → AFD",
        width=22,
        command=convertir_a_afd
    ).pack(
        pady=3
    )

    tk.Button(
        panel,
        text="Minimizar AFD",
        width=22,
        command=minimizar_afd
    ).pack(
        pady=3
    )

    # ============================================================
    # LIMPIAR
    # ============================================================

    tk.Button(
        panel,
        text="Limpiar autómata",
        width=22,
        command=limpiar_automata
    ).pack(
        pady=(15, 5)
    )

    # ============================================================
    # MENSAJE
    # ============================================================

    etiqueta_mensaje = tk.Label(
        panel,
        text="Listo para comenzar.",
        bg="#eeeeee",
        wraplength=280,
        justify="center",
        font=("Arial", 9)
    )

    etiqueta_mensaje.pack(
        pady=10
    )

    # ============================================================
    # PANEL DERECHO
    # ============================================================

    marco_derecho = tk.Frame(
        ventana,
        bg="white"
    )

    marco_derecho.pack(
        side=tk.RIGHT,
        fill=tk.BOTH,
        expand=True
    )

    etiqueta_resultado = tk.Label(
        marco_derecho,
        text="",
        font=("Arial", 16, "bold"),
        bg="white"
    )

    etiqueta_resultado.pack(
        pady=15
    )

    # ============================================================
    # ÁREA DEL AUTÓMATA
    # ============================================================

    marco_canvas = tk.Frame(
        marco_derecho,
        bg="white"
    )

    marco_canvas.pack(
        fill=tk.BOTH,
        expand=True
    )

    # ------------------------------------------------------------
    # CANVAS
    # ------------------------------------------------------------

    canvas = tk.Canvas(
        marco_canvas,
        bg="white",
        highlightthickness=0
    )

    canvas.pack(
        side=tk.TOP,
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=(10, 0)
    )

    # ------------------------------------------------------------
    # BARRA VERTICAL
    # ------------------------------------------------------------

    scrollbar_derecha = tk.Scrollbar(
        marco_canvas,
        orient=tk.VERTICAL,
        command=canvas.yview
    )

    scrollbar_derecha.pack(
        side=tk.RIGHT,
        fill=tk.Y,
        pady=(10, 0)
    )

    # ------------------------------------------------------------
    # BARRA HORIZONTAL
    # ------------------------------------------------------------

    scrollbar_horizontal = tk.Scrollbar(
        marco_derecho,
        orient=tk.HORIZONTAL,
        command=canvas.xview
    )

    scrollbar_horizontal.pack(
        side=tk.BOTTOM,
        fill=tk.X,
        padx=10,
        pady=(0, 10)
    )

    # ------------------------------------------------------------
    # CONECTAR SCROLLBARS
    # ------------------------------------------------------------

    canvas.configure(
        yscrollcommand=scrollbar_derecha.set,
        xscrollcommand=scrollbar_horizontal.set
    )

    # ============================================================
    # ACTUALIZAR ÁREA DE DESPLAZAMIENTO
    # ============================================================

    def actualizar_scroll_derecho():

        ancho_visible = canvas.winfo_width()
        alto_visible = canvas.winfo_height()

        if ancho_visible <= 1:
            ancho_visible = 800

        if alto_visible <= 1:
            alto_visible = 600

        ancho_maximo = max(
            ancho_visible,
            1000
        )

        alto_maximo = max(
            alto_visible,
            650
        )

        if posiciones:

            ancho_necesario = max(
                x
                for x, y in posiciones.values()
            ) + 180

            alto_necesario = max(
                y
                for x, y in posiciones.values()
            ) + 180

            ancho_maximo = max(
                ancho_maximo,
                ancho_necesario
            )

            alto_maximo = max(
                alto_maximo,
                alto_necesario
            )

        canvas.configure(
            scrollregion=(
                0,
                0,
                ancho_maximo,
                alto_maximo
            )
        )

    # ============================================================
    # ACTUALIZAR SCROLL AL CAMBIAR TAMAÑO
    # ============================================================

    def actualizar_canvas(event=None):

        centrar_titulo()
        actualizar_scroll_derecho()

    canvas.bind(
        "<Configure>",
        actualizar_canvas
    )

    # ============================================================
    # INICIAR
    # ============================================================

    ventana.update_idletasks()

    dibujar_automata()
    actualizar_scroll_derecho()

    ventana.mainloop()


# ================================================================
# EJECUCIÓN PRINCIPAL
# ================================================================

if __name__ == "__main__":
    iniciar_interfaz()