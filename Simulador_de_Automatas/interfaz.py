import tkinter as tk
from tkinter import messagebox
from automata import Automata


def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Simulador de Autómatas")
    ventana.geometry("1150x750")
    ventana.minsize(950, 650)

    # ==========================================
    # AUTÓMATA
    # ==========================================

    automata = Automata()

    # Guardar la posición visual de cada estado
    posiciones = {}

    # ==========================================
    # FUNCIONES
    # ==========================================

    def agregar_estado():
        estado = entrada_estado.get().strip()

        if not estado:
            messagebox.showwarning(
                "Dato inválido",
                "Ingrese un nombre para el estado."
            )
            return

        if estado in automata.estados:
            messagebox.showwarning(
                "Estado existente",
                f"El estado {estado} ya existe."
            )
            return

        # Guardar estado en el autómata
        automata.agregar_estado(estado)

        # Calcular posición
        numero = len(posiciones)

        x = 120 + (numero % 4) * 220
        y = 120 + (numero // 4) * 160

        posiciones[estado] = (x, y)

        # Dibujar estado
        radio = 35

        canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            outline="black",
            width=2
        )

        # Dibujar nombre
        canvas.create_text(
            x,
            y,
            text=estado,
            font=("Arial", 12, "bold")
        )

        entrada_estado.delete(0, tk.END)

    def agregar_simbolo():
        simbolo = entrada_simbolo.get().strip()

        if not simbolo:
            messagebox.showwarning(
                "Dato inválido",
                "Ingrese un símbolo."
            )
            return

        if simbolo == "ε":
            messagebox.showwarning(
                "Símbolo no válido",
                "ε se utiliza únicamente para transiciones epsilon."
            )
            return

        if simbolo in automata.alfabeto:
            messagebox.showwarning(
                "Símbolo existente",
                f"El símbolo {simbolo} ya existe."
            )
            return

        # Guardar símbolo
        automata.agregar_simbolo(simbolo)

        entrada_simbolo.delete(0, tk.END)

        messagebox.showinfo(
            "Símbolo agregado",
            f"El símbolo {simbolo} fue agregado al alfabeto."
        )

    def agregar_transicion():
        origen = entrada_origen.get().strip()
        simbolo = entrada_transicion.get().strip()
        destino = entrada_destino.get().strip()

        # Permitir escribir "e" para epsilon
        if simbolo.lower() == "e":
            simbolo = "ε"

        # Validar campos
        if not origen or not simbolo or not destino:
            messagebox.showwarning(
                "Datos incompletos",
                "Complete origen, símbolo y destino."
            )
            return

        # Validar estado origen
        if origen not in automata.estados:
            messagebox.showwarning(
                "Estado inválido",
                f"El estado {origen} no existe."
            )
            return

        # Validar estado destino
        if destino not in automata.estados:
            messagebox.showwarning(
                "Estado inválido",
                f"El estado {destino} no existe."
            )
            return

        # Validar símbolo
        if simbolo != "ε" and simbolo not in automata.alfabeto:
            messagebox.showwarning(
                "Símbolo inválido",
                f"El símbolo {simbolo} no pertenece al alfabeto."
            )
            return

        # Guardar transición
        automata.agregar_transicion(
            origen,
            simbolo,
            destino
        )

        # Posición de origen y destino
        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]

        radio = 35

        dx = x2 - x1
        dy = y2 - y1
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        # ==========================================
        # TRANSICIÓN A OTRO ESTADO
        # ==========================================

        if distancia != 0:

            # Punto de inicio en el borde
            inicio_x = x1 + (dx / distancia) * radio
            inicio_y = y1 + (dy / distancia) * radio

            # Punto final en el borde
            fin_x = x2 - (dx / distancia) * radio
            fin_y = y2 - (dy / distancia) * radio

            # Dibujar flecha
            canvas.create_line(
                inicio_x,
                inicio_y,
                fin_x,
                fin_y,
                arrow=tk.LAST,
                width=2
            )

            # Punto medio
            xm = (inicio_x + fin_x) / 2
            ym = (inicio_y + fin_y) / 2

            # Dibujar símbolo
            canvas.create_text(
                xm,
                ym - 12,
                text=simbolo,
                font=("Arial", 12, "bold")
            )

        # ==========================================
        # TRANSICIÓN DEL ESTADO HACIA SÍ MISMO
        # ==========================================

        else:

            canvas.create_arc(
                x1 - 30,
                y1 - 75,
                x1 + 30,
                y1 - 15,
                start=30,
                extent=300,
                style=tk.ARC,
                width=2
            )

            canvas.create_text(
                x1,
                y1 - 80,
                text=simbolo,
                font=("Arial", 12, "bold")
            )

        # Limpiar campos
        entrada_origen.delete(0, tk.END)
        entrada_transicion.delete(0, tk.END)
        entrada_destino.delete(0, tk.END)

    def definir_inicial():
        estado = entrada_inicial.get().strip()

        if not estado:
            messagebox.showwarning(
                "Dato inválido",
                "Ingrese el estado inicial."
            )
            return

        if estado not in automata.estados:
            messagebox.showwarning(
                "Estado inválido",
                f"El estado {estado} no existe."
            )
            return

        # Definir estado inicial
        automata.definir_inicial(estado)

        # Obtener posición
        x, y = posiciones[estado]

        # Dibujar flecha de inicio
        canvas.create_line(
            x - 80,
            y,
            x - 40,
            y,
            arrow=tk.LAST,
            width=2
        )

        entrada_inicial.delete(0, tk.END)

        messagebox.showinfo(
            "Estado inicial",
            f"{estado} es ahora el estado inicial."
        )

    def definir_final():
        estado = entrada_final.get().strip()

        if not estado:
            messagebox.showwarning(
                "Dato inválido",
                "Ingrese el estado final."
            )
            return

        if estado not in automata.estados:
            messagebox.showwarning(
                "Estado inválido",
                f"El estado {estado} no existe."
            )
            return

        if estado in automata.estados_finales:
            messagebox.showwarning(
                "Estado final existente",
                f"{estado} ya es un estado final."
            )
            return

        # Guardar como estado final
        automata.agregar_final(estado)

        # Obtener posición
        x, y = posiciones[estado]

        # Segundo círculo
        radio = 41

        canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            outline="black",
            width=2
        )

        entrada_final.delete(0, tk.END)

        messagebox.showinfo(
            "Estado final",
            f"{estado} ahora es un estado final."
        )

    def simular_cadena():
        cadena = entrada_cadena.get()

        # Verificar estado inicial
        if automata.estado_inicial is None:
            messagebox.showwarning(
                "Autómata incompleto",
                "Primero debe definir el estado inicial."
            )
            return

        # Verificar estados finales
        if not automata.estados_finales:
            messagebox.showwarning(
                "Autómata incompleto",
                "Primero debe definir al menos un estado final."
            )
            return

        try:
            # Ejecutar la simulación real
            aceptada = automata.simular(cadena)

            if aceptada:
                resultado.config(
                    text="Resultado: ✅ ACEPTADA"
                )
            else:
                resultado.config(
                    text="Resultado: ❌ RECHAZADA"
                )

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    # ==========================================
    # TÍTULO
    # ==========================================

    titulo = tk.Label(
        ventana,
        text="SIMULADOR DE AUTÓMATAS",
        font=("Arial", 24, "bold")
    )

    titulo.pack(pady=20)

    # ==========================================
    # CONTENEDOR PRINCIPAL
    # ==========================================

    contenido = tk.Frame(ventana)

    contenido.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # ==========================================
    # PANEL IZQUIERDO
    # ==========================================

    panel_control = tk.LabelFrame(
        contenido,
        text="Configuración del autómata",
        padx=5,
        pady=5,
        width=310
    )

    panel_control.pack(
        side="left",
        fill="y",
        padx=(0, 10)
    )

    panel_control.pack_propagate(False)

    # ==========================================
    # PANEL CON DESPLAZAMIENTO
    # ==========================================

    canvas_control = tk.Canvas(
        panel_control,
        highlightthickness=0
    )

    scrollbar_control = tk.Scrollbar(
        panel_control,
        orient="vertical",
        command=canvas_control.yview
    )

    canvas_control.configure(
        yscrollcommand=scrollbar_control.set
    )

    canvas_control.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_control.pack(
        side="right",
        fill="y"
    )

    # Frame de controles
    panel_formulario = tk.Frame(
        canvas_control
    )

    ventana_controles = canvas_control.create_window(
        (0, 0),
        window=panel_formulario,
        anchor="nw"
    )

    # ==========================================
    # ACTUALIZAR SCROLL
    # ==========================================

    def actualizar_scrollregion(event=None):
        canvas_control.configure(
            scrollregion=canvas_control.bbox("all")
        )

        canvas_control.itemconfig(
            ventana_controles,
            width=canvas_control.winfo_width()
        )

    panel_formulario.bind(
        "<Configure>",
        actualizar_scrollregion
    )

    canvas_control.bind(
        "<Configure>",
        actualizar_scrollregion
    )

    # ==========================================
    # RUEDA DEL MOUSE
    # ==========================================

    def desplazar_rueda(event):
        canvas_control.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas_control.bind_all(
        "<MouseWheel>",
        desplazar_rueda
    )

    # ==========================================
    # PANEL DERECHO - DIAGRAMA
    # ==========================================

    panel_diagrama = tk.LabelFrame(
        contenido,
        text="Diagrama del autómata",
        padx=10,
        pady=10
    )

    panel_diagrama.pack(
        side="right",
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        panel_diagrama,
        bg="white"
    )

    canvas.pack(
        fill="both",
        expand=True
    )

    # ==========================================
    # ESTADO
    # ==========================================

    tk.Label(
        panel_formulario,
        text="Estado"
    ).pack(
        anchor="w",
        padx=15,
        pady=(10, 0)
    )

    entrada_estado = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_estado.pack(
        pady=(0, 10),
        padx=15
    )

    boton_estado = tk.Button(
        panel_formulario,
        text="Agregar estado",
        width=22,
        command=agregar_estado
    )

    boton_estado.pack(
        pady=(0, 20),
        padx=15
    )

    # ==========================================
    # ESTADO INICIAL
    # ==========================================

    tk.Label(
        panel_formulario,
        text="Estado inicial"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_inicial = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_inicial.pack(
        pady=(0, 10),
        padx=15
    )

    boton_inicial = tk.Button(
        panel_formulario,
        text="Definir estado inicial",
        width=22,
        command=definir_inicial
    )

    boton_inicial.pack(
        pady=(0, 20),
        padx=15
    )

    # ==========================================
    # ESTADO FINAL
    # ==========================================

    tk.Label(
        panel_formulario,
        text="Estado final"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_final = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_final.pack(
        pady=(0, 10),
        padx=15
    )

    boton_final = tk.Button(
        panel_formulario,
        text="Definir estado final",
        width=22,
        command=definir_final
    )

    boton_final.pack(
        pady=(0, 20),
        padx=15
    )

    # ==========================================
    # SÍMBOLO
    # ==========================================

    tk.Label(
        panel_formulario,
        text="Símbolo"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_simbolo = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_simbolo.pack(
        pady=(0, 10),
        padx=15
    )

    boton_simbolo = tk.Button(
        panel_formulario,
        text="Agregar símbolo",
        width=22,
        command=agregar_simbolo
    )

    boton_simbolo.pack(
        pady=(0, 20),
        padx=15
    )

    # ==========================================
    # TRANSICIÓN
    # ==========================================

    tk.Label(
        panel_formulario,
        text="TRANSICIÓN"
    ).pack(
        anchor="w",
        padx=15,
        pady=(5, 5)
    )

    tk.Label(
        panel_formulario,
        text="Origen"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_origen = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_origen.pack(
        pady=(0, 5),
        padx=15
    )

    tk.Label(
        panel_formulario,
        text="Símbolo"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_transicion = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_transicion.pack(
        pady=(0, 5),
        padx=15
    )

    tk.Label(
        panel_formulario,
        text="Destino"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_destino = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_destino.pack(
        pady=(0, 10),
        padx=15
    )

    boton_transicion = tk.Button(
        panel_formulario,
        text="Agregar transición",
        width=22,
        command=agregar_transicion
    )

    boton_transicion.pack(
        pady=(0, 20),
        padx=15
    )

    # ==========================================
    # SIMULACIÓN
    # ==========================================

    tk.Label(
        panel_formulario,
        text="Cadena a simular"
    ).pack(
        anchor="w",
        padx=15
    )

    entrada_cadena = tk.Entry(
        panel_formulario,
        width=27
    )

    entrada_cadena.pack(
        pady=(0, 10),
        padx=15
    )

    boton_simular = tk.Button(
        panel_formulario,
        text="SIMULAR",
        width=22,
        command=simular_cadena
    )

    boton_simular.pack(
        pady=(0, 15),
        padx=15
    )

    resultado = tk.Label(
        panel_formulario,
        text="Resultado: ---",
        font=("Arial", 12, "bold")
    )

    resultado.pack(
        pady=(5, 20),
        padx=15
    )

    # ==========================================
    # INICIAR INTERFAZ
    # ==========================================

    ventana.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()