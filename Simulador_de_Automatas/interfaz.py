import tkinter as tk
from tkinter import messagebox
from automata import Automata


def iniciar_interfaz():

    automata = Automata()
    posiciones = {}
    modo_actual = "AFN / AFD"

    # ============================================================
    # VENTANA PRINCIPAL
    # ============================================================

    ventana = tk.Tk()
    ventana.title("Simulador de Autómatas")
    ventana.geometry("1000x650")
    ventana.minsize(900, 550)

    # ============================================================
    # FUNCIONES AUXILIARES
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
    # CENTRAR TÍTULO DEL ÁREA DE DIBUJO
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
            25
        )

    # ============================================================
    # DIBUJAR AUTOMATA
    # ============================================================

    def dibujar_automata():

        canvas.delete("all")

        # Obtener el ancho actual del área de dibujo
        ancho_canvas = canvas.winfo_width()

        if ancho_canvas <= 1:
            ancho_canvas = 650

        # ========================================================
        # TÍTULO CENTRADO
        # ========================================================

        canvas.create_text(
            ancho_canvas / 2,
            25,
            text=f"Visualización: {modo_actual}",
            font=("Arial", 16, "bold"),
            anchor="center",
            tags="titulo"
        )

        # ========================================================
        # AGRUPAR BUCLES POR ESTADO
        # ========================================================

        bucles = {}

        for (origen, simbolo), destinos in automata.transiciones.items():

            if origen not in posiciones:
                continue

            if origen in destinos:

                if origen not in bucles:
                    bucles[origen] = []

                bucles[origen].append(
                    simbolo_visual(simbolo)
                )

        # ========================================================
        # DIBUJAR TRANSICIONES NORMALES
        # ========================================================

        for (origen, simbolo), destinos in automata.transiciones.items():

            if origen not in posiciones:
                continue

            x1, y1 = posiciones[origen]

            for destino in destinos:

                if destino not in posiciones:
                    continue

                # Los bucles se dibujan aparte
                if origen == destino:
                    continue

                x2, y2 = posiciones[destino]

                canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    arrow=tk.LAST,
                    width=2
                )

                # Texto de transición
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2

                canvas.create_text(
                    mx,
                    my - 12,
                    text=simbolo_visual(simbolo),
                    font=("Arial", 11, "bold")
                )

        # ========================================================
        # DIBUJAR BUCLES
        # ========================================================

        for estado, simbolos in bucles.items():

            x, y = posiciones[estado]

            # Un solo bucle por estado
            canvas.create_oval(
                x - 35,
                y - 65,
                x + 35,
                y - 5,
                outline="black",
                width=2
            )

            # Mostrar todos los símbolos del bucle
            texto_bucle = ", ".join(simbolos)

            canvas.create_text(
                x,
                y - 75,
                text=texto_bucle,
                font=("Arial", 11, "bold")
            )

        # ========================================================
        # DIBUJAR ESTADOS
        # ========================================================

        for estado, (x, y) in posiciones.items():

            # Estado inicial
            if estado == automata.estado_inicial:

                canvas.create_line(
                    x - 70,
                    y,
                    x - 40,
                    y,
                    arrow=tk.LAST,
                    width=2
                )

            # Estado
            canvas.create_oval(
                x - 40,
                y - 40,
                x + 40,
                y + 40,
                fill="white",
                outline="black",
                width=2
            )

            # Estado final
            if estado in automata.estados_finales:

                canvas.create_oval(
                    x - 34,
                    y - 34,
                    x + 34,
                    y + 34,
                    outline="black",
                    width=2
                )

            canvas.create_text(
                x,
                y,
                text=estado,
                font=("Arial", 11, "bold")
            )

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

        automata.agregar_estado(estado)

        cantidad = len(posiciones)

        columnas = 4

        x = 120 + (cantidad % columnas) * 180
        y = 150 + (cantidad // columnas) * 150

        posiciones[estado] = (x, y)

        entrada_estado.delete(0, tk.END)

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

        simbolo = normalizar_simbolo(simbolo)

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

        automata.agregar_simbolo(simbolo)

        entrada_simbolo.delete(0, tk.END)

        mostrar_mensaje(
            f"Símbolo '{simbolo}' agregado correctamente."
        )

    # ============================================================
    # AGREGAR TRANSICIÓN
    # ============================================================

    def agregar_transicion():

        origen = entrada_origen.get().strip()
        simbolo = entrada_transicion.get().strip()
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

        simbolo = normalizar_simbolo(simbolo)

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

        entrada_origen.delete(0, tk.END)
        entrada_transicion.delete(0, tk.END)
        entrada_destino.delete(0, tk.END)

        mostrar_mensaje(
            f"Transición agregada: "
            f"{origen} --{simbolo_visual(simbolo)}--> {destino}"
        )

        dibujar_automata()

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

            automata.definir_inicial(estado)

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )
            return

        entrada_inicial.delete(0, tk.END)

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

            automata.agregar_final(estado)

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )
            return

        entrada_final.delete(0, tk.END)

        mostrar_mensaje(
            f"Estado final: {estado}"
        )

        dibujar_automata()

    # ============================================================
    # SIMULAR CADENA
    # ============================================================

    def simular_cadena():

        cadena = entrada_cadena.get()

        try:

            resultado = automata.simular(cadena)

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
    # CONVERTIR AFN → AFD
    # ============================================================

    def convertir_a_afd():

        nonlocal automata, posiciones, modo_actual

        try:

            afd = automata.convertir_a_afd()

        except ValueError as error:

            messagebox.showerror(
                "Error de conversión",
                str(error)
            )
            return

        automata = afd
        modo_actual = "AFD CONVERTIDO"

        posiciones.clear()

        estados = sorted(automata.estados)

        columnas = 3

        for i, estado in enumerate(estados):

            x = 150 + (i % columnas) * 280
            y = 150 + (i // columnas) * 180

            posiciones[estado] = (x, y)

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

        nonlocal automata, posiciones, modo_actual

        try:

            afd_minimo = automata.minimizar_afd()

        except Exception as error:

            messagebox.showerror(
                "Error de minimización",
                str(error)
            )
            return

        automata = afd_minimo
        modo_actual = "AFD MINIMIZADO"

        posiciones.clear()

        estados = sorted(automata.estados)

        columnas = 3

        for i, estado in enumerate(estados):

            x = 150 + (i % columnas) * 280
            y = 150 + (i // columnas) * 180

            posiciones[estado] = (x, y)

        etiqueta_resultado.config(
            text=""
        )

        mostrar_mensaje(
            "AFD minimizado correctamente."
        )

        dibujar_automata()

    # ============================================================
    # LIMPIAR AUTOMATA
    # ============================================================

    def limpiar_automata():

        nonlocal automata, posiciones, modo_actual

        respuesta = messagebox.askyesno(
            "Limpiar",
            "¿Desea eliminar el autómata actual?"
        )

        if not respuesta:
            return

        automata = Automata()
        posiciones.clear()
        modo_actual = "AFN / AFD"

        etiqueta_resultado.config(
            text=""
        )

        mostrar_mensaje(
            "Autómata limpiado."
        )

        dibujar_automata()

    # ============================================================
    # PANEL IZQUIERDO CON DESPLAZAMIENTO
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

    # Canvas del panel
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

    # Barra de desplazamiento
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

    # Panel interno
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
            scrollregion=canvas_panel.bbox("all")
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

    # Desplazamiento con rueda del mouse
    def desplazamiento_mouse(event):

        canvas_panel.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas_panel.bind_all(
        "<MouseWheel>",
        desplazamiento_mouse
    )

    # ============================================================
    # CONTROLES DEL PANEL
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

    # ------------------------------------------------------------
    # ESTADOS
    # ------------------------------------------------------------

    tk.Label(
        panel,
        text="Agregar estado",
        font=("Arial", 11, "bold"),
        bg="#eeeeee"
    ).pack()

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

    # ------------------------------------------------------------
    # ESTADO INICIAL
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # ESTADO FINAL
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # ALFABETO
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # TRANSICIÓN
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # SIMULACIÓN
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # TRANSFORMACIONES
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # LIMPIAR
    # ------------------------------------------------------------

    tk.Button(
        panel,
        text="Limpiar autómata",
        width=22,
        command=limpiar_automata
    ).pack(
        pady=(15, 5)
    )

    # ------------------------------------------------------------
    # MENSAJE
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # RESULTADO
    # ------------------------------------------------------------

    etiqueta_resultado = tk.Label(
        marco_derecho,
        text="",
        font=("Arial", 16, "bold"),
        bg="white"
    )

    etiqueta_resultado.pack(
        pady=15
    )

    # ------------------------------------------------------------
    # CANVAS DEL AUTOMATA
    # ------------------------------------------------------------

    canvas = tk.Canvas(
        marco_derecho,
        bg="white"
    )

    canvas.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
    )

    # Actualizar posición del título cuando cambie
    # el tamaño del área de dibujo
    canvas.bind(
        "<Configure>",
        centrar_titulo
    )

    # ============================================================
    # INICIAR
    # ============================================================

    dibujar_automata()

    ventana.mainloop()


# ================================================================
# EJECUCIÓN
# ================================================================

if __name__ == "__main__":
    iniciar_interfaz()