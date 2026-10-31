"""Validación de registros mediante regex y comprobación de fecha real."""
import re
from datetime import datetime

PATRON_LOG = r"(?P<fecha>[0-9]{4}-[0-9]{2}-[0-9]{2}) (?P<hora>[0-9]{2}:[0-9]{2}:[0-9]{2}) \[(?P<nivel>DEBUG|INFO|WARNING|ERROR|CRITICAL)\] (?P<mensaje>\S[^\r\n]*)"
REGEX_LOG = re.compile(PATRON_LOG)
EJEMPLO_LOGS = """2026-10-31 08:00:00 [INFO] Inicio del sistema
2026-10-31 08:01:15 [WARNING] Intento de acceso fallido
2026-10-31 08:02:30 [ERROR] No se pudo abrir el archivo
2026-02-30 08:03:00 [INFO] Fecha inexistente
2026-10-31 25:00:00 [INFO] Hora incorrecta
2026-10-31 08:04:00 [OTRO] Nivel no permitido
Línea que no tiene formato de log"""


def validar_linea(linea):
    """Devuelve (válida, detalle). No modifica el texto recibido."""
    coincidencia = REGEX_LOG.fullmatch(linea)
    if coincidencia is None:
        return False, "Formato incorrecto: AAAA-MM-DD HH:MM:SS [NIVEL] Mensaje; revise nivel y mensaje."
    try:
        datetime.strptime(coincidencia['fecha'] + ' ' + coincidencia['hora'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False, "Fecha u hora inexistente o fuera de rango."
    return True, 'Registro válido — ' + coincidencia['nivel']


def validar_logs(texto):
    """Omite líneas vacías y conserva los números de línea originales."""
    if not isinstance(texto, str):
        raise ValueError('Los logs deben ser texto.')
    resultados = []
    for numero, linea in enumerate(texto.splitlines(), 1):
        if not linea.strip():
            continue
        valido, detalle = validar_linea(linea)
        resultados.append({'linea': numero, 'texto': linea, 'valido': valido, 'detalle': detalle})
    return resultados


def abrir_validador(ventana):
    """Ventana independiente integrada en la aplicación Tkinter."""
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText
    from pathlib import Path

    dialogo = tk.Toplevel(ventana)
    dialogo.title('Validación de logs')
    dialogo.geometry('950x700')
    dialogo.minsize(650, 500)
    dialogo.columnconfigure(0, weight=1)
    dialogo.rowconfigure(3, weight=1)
    dialogo.rowconfigure(6, weight=1)
    tk.Label(dialogo, text='VALIDACIÓN DE LOGS', font=('Arial', 16, 'bold')).grid(row=0, column=0, pady=(12, 6))
    tk.Label(dialogo, text='Formato: AAAA-MM-DD HH:MM:SS [NIVEL] Mensaje\nNiveles: DEBUG, INFO, WARNING, ERROR, CRITICAL (mayúsculas).\nSe omiten las líneas vacías; se comprueba que fecha y hora existan.', justify='left').grid(row=1, column=0, sticky='w', padx=12)
    barra = tk.Frame(dialogo)
    barra.grid(row=2, column=0, sticky='ew', padx=12, pady=8)
    entrada = ScrolledText(dialogo, height=10, wrap='none', undo=True)
    entrada.grid(row=3, column=0, sticky='nsew', padx=12)
    resumen = tk.StringVar(value='Pegue los registros o cargue un archivo .log / .txt en UTF-8.')
    tk.Label(dialogo, textvariable=resumen, anchor='w').grid(row=5, column=0, sticky='ew', padx=12, pady=8)
    salida = ScrolledText(dialogo, height=10, wrap='word', state='disabled')
    salida.grid(row=6, column=0, sticky='nsew', padx=12, pady=(0, 12))

    def escribir_resultado(texto):
        salida.config(state='normal')
        salida.delete('1.0', tk.END)
        salida.insert('1.0', texto)
        salida.config(state='disabled')

    def cambiar_entrada(texto):
        entrada.delete('1.0', tk.END)
        entrada.insert('1.0', texto)
        escribir_resultado('')
        resumen.set('Contenido cargado. Pulse Validar logs.')

    def cargar():
        nombre = filedialog.askopenfilename(parent=dialogo, title='Abrir registros', filetypes=[('Logs y texto', '*.log *.txt'), ('Todos los archivos', '*.*')])
        if not nombre:
            return
        try:
            ruta = Path(nombre)
            if ruta.stat().st_size > 2 * 1024 * 1024:
                raise ValueError('Seleccione un archivo de hasta 2 MB.')
            texto = ruta.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError, ValueError) as error:
            messagebox.showerror('No se pudo abrir el archivo', str(error), parent=dialogo)
            return
        cambiar_entrada(texto)

    def validar():
        texto = entrada.get('1.0', 'end-1c')
        if len(texto) > 2 * 1024 * 1024:
            messagebox.showerror('Texto demasiado grande', 'Use hasta 2 millones de caracteres.', parent=dialogo)
            return
        resultados = validar_logs(texto)
        aceptados = sum(r['valido'] for r in resultados)
        resumen.set(f'Total: {len(resultados)} | Válidos: {aceptados} | Inválidos: {len(resultados) - aceptados}')
        escribir_resultado('\n\n'.join(
            f"Línea {r['linea']} — {'VÁLIDO' if r['valido'] else 'INVÁLIDO'}\n{r['detalle']}\n{r['texto']}"
            for r in resultados) if resultados else 'No hay registros para validar.')

    def ver_patron():
        messagebox.showinfo('Expresión regular utilizada', PATRON_LOG + '\n\nSe aplica fullmatch a cada línea. Después se valida la fecha y hora con datetime.\nEste módulo utiliza re de Python; el constructor de autómatas utiliza Thompson y admite una sintaxis más limitada.', parent=dialogo)

    tk.Button(barra, text='Cargar archivo', command=cargar).pack(side='left', padx=(0, 6))
    tk.Button(barra, text='Cargar ejemplo', command=lambda: cambiar_entrada(EJEMPLO_LOGS)).pack(side='left', padx=6)
    tk.Button(barra, text='Ver regex', command=ver_patron).pack(side='left', padx=6)
    tk.Button(barra, text='Limpiar', command=lambda: cambiar_entrada('')).pack(side='left', padx=6)
    tk.Button(dialogo, text='Validar logs', command=validar).grid(row=4, column=0, pady=(10, 0))
