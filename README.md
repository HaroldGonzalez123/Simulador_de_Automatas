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
