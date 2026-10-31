# Simulador de Autómatas — versión corregida

## Abrir en Windows
1. Extraiga todo el ZIP (no ejecute desde dentro del archivo comprimido).
2. Entre en la carpeta Simulador_de_Automatas-main y después en Simulador_de_Automatas.
3. Abra una terminal en esa carpeta y ejecute `python interfaz.py`.
   Si su instalación utiliza el lanzador de Windows, puede usar `py interfaz.py`.
4. También puede abrir la solución .sln en Visual Studio con soporte de Python.
   El archivo de inicio configurado es interfaz.py.

Necesita Python 3 con Tkinter. No requiere paquetes de pip adicionales.
Si `python` no se reconoce, configure el intérprete de Python en su equipo.
Para verificar Tkinter use `python -m tkinter`.

## Ejemplo guiado: cadenas binarias que terminan en 01
1. En «Expresión regular», escriba `(0|1)*01`.
2. Pulse «Generar AFN desde Regex». Se dibujará el AFN con transiciones ε.
3. En «Simular cadena», escriba una cadena y pulse «Simular».
   - 01, 101 y 1101: aceptadas.
   - 10, 111 y la cadena vacía: rechazadas.
4. Pulse «Convertir AFN → AFD». Los nuevos estados se llaman D0, D1, etc.
5. Pruebe las mismas cadenas: deben mantener los mismos resultados.
6. Pulse «Minimizar AFD». Este ejemplo debe quedar con tres estados M0, M1 y M2.
7. Repita las pruebas. El lenguaje aceptado debe seguir siendo el mismo.

Puede pulsar «Minimizar AFD» directamente sobre un AFN: ahora se determiniza
antes de minimizar. Cada transformación sustituye el autómata que está en pantalla.
Generar otra expresión también sustituye el autómata actual.

## Crear un autómata manualmente
Ejemplo: aceptar exactamente una letra a.
1. Agregue q0 y q1 por separado con «Agregar estado».
2. Escriba q0 en «Estado inicial» y pulse «Definir inicial».
3. Escriba q1 en «Estado final» y pulse «Agregar final».
4. Agregue a en «Símbolo del alfabeto».
5. En la transición, escriba origen q0, símbolo a y destino q1.
6. Pulse «Agregar transición».
7. Simule a (aceptada), aa (rechazada) y el campo vacío (rechazado).
8. Para comenzar otro ejercicio, pulse «Limpiar autómata».

## Sintaxis de expresiones regulares
- `|`: unión, por ejemplo a|b.
- `*`: cero o más repeticiones, por ejemplo a*.
- Paréntesis: agrupación, por ejemplo a(b|c).
- Concatenación: símbolos juntos, como ab o (a|b)(c|d).
- `e` y `ε`: épsilon, es decir, cadena vacía. Están reservados y no son letras del alfabeto.
- Para probar la cadena vacía, deje vacío «Simular cadena»; no escriba e ni ε.
- Los espacios se eliminan de la expresión. Los símbolos se procesan de uno en uno.
- No se admite la sintaxis avanzada de regex de Python (clases, escapes, +, ?, etc.).
  Los caracteres no reservados se interpretan como literales. Use ab, no a·b.

## Consola y pruebas
- Consola: `python Simulador_de_Automatas.py`.
- Pruebas: `python -m unittest -v test_simulador`.

## Correcciones realizadas
- Concatenación antes de grupos: a(b|c), (a|b)(c|d), a*(b|c).
- Tratamiento coherente de e/ε en regex, interfaz, consola y motor.
- Minimización mediante particiones después de determinizar y completar el AFD.
- Estado pozo para transiciones faltantes y conservación de todo el alfabeto.
- Nombres únicos D0, D1, etc. para conjuntos de estados de la conversión.
- La consola conserva el resultado de convertir o minimizar para seguir probándolo.
- Pruebas de regresión, entradas inválidas y 80 AFN generados con semilla fija.

Validación realizada: cinco pruebas automatizadas satisfactorias, con 13,348
comparaciones de aceptación, además de comprobaciones de errores y minimalidad.
Los archivos Python compilan. La ventana no se ha verificado visualmente en este entorno.

## Desplazamiento de la ventana
Se reservó espacio para las barras verticales del panel y del diagrama.
Use la barra junto al panel gris, la rueda del mouse sobre ese panel, o las
teclas Av Pág / Re Pág para bajar o subir los controles. También se manejan
los movimientos pequeños del panel táctil.

## Validación de logs (nuevo módulo)
El requisito recibido solo dice «Validación de logs», sin especificar formato.
Se adoptó el siguiente formato de ejemplo; debe confirmarse con el catedrático:

`AAAA-MM-DD HH:MM:SS [NIVEL] Mensaje`

Ejemplo válido: `2026-10-31 08:00:00 [INFO] Inicio del sistema`.
Niveles permitidos: DEBUG, INFO, WARNING, ERROR y CRITICAL en mayúsculas.
Debe haber un espacio entre fecha, hora, nivel y mensaje; el mensaje no puede
estar vacío ni empezar con espacios. Las líneas vacías se omiten.

1. Abra interfaz.py y pulse «Validación de logs» en la parte superior del panel.
2. Pulse «Cargar ejemplo», pegue registros o use «Cargar archivo» (.log/.txt UTF-8).
3. Pulse «Validar logs». El ejemplo incluido devuelve 3 válidos y 4 inválidos.
4. Revise cada número de línea, resultado y motivo del rechazo.
5. «Ver regex» muestra el patrón que se utiliza para validar el formato.

Arquitectura: logs.py separa validar_linea / validar_logs de la ventana Tkinter.
El módulo usa re.fullmatch para comprobar toda la línea y datetime para validar
fechas y horas reales. La regex por sí sola no detecta fechas inexistentes.
No modifica los archivos cargados. Admite archivos de hasta 2 MB.
El módulo de logs utiliza la sintaxis de regex de Python; el generador de
AFN utiliza Thompson y su sintaxis limitada. No pegue el patrón de logs en el
campo «Expresión regular» del simulador de autómatas.

Pruebas completas: `python -m unittest -v test_simulador test_logs` desde la
carpeta que contiene interfaz.py. Nueve pruebas automatizadas pasan, incluyendo
los 13,348 contrastes de aceptación existentes. La nueva ventana de logs
requiere comprobación visual en Windows.

Actualización: use el proyecto completo de este ZIP. Si reemplaza archivos
individualmente, copie interfaz.py, logs.py, test_logs.py y el .pyproj actualizado;
actualice también este README. Suba estos cambios al repositorio conservando
las rutas existentes. La documentación técnica/administrativa y presentación
final se preparan por separado.
