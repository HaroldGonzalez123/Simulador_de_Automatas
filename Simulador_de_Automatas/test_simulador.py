import itertools
import random
import re
import unittest
from automata import Automata
from expresiones import ExpresionRegular


def cadenas(alfabeto, longitud):
    for n in range(longitud + 1):
        for letras in itertools.product(alfabeto, repeat=n):
            yield ''.join(letras)


class PruebasSimulador(unittest.TestCase):
    def test_regex_y_transformaciones(self):
        casos = ['a', 'ab', 'a|b', 'a*', '(a|b)*abb', '(0|1)*01',
                 'a(b|c)', '(a|b)(c|d)', 'a*(b|c)', '(ab)*',
                 '((a|b)*a)*', 'ε', 'e', 'aεb', '(a|ε)*']
        self.comprobaciones = 0
        for regex in casos:
            alfabeto = sorted(set(regex) - set('()|*eε'))
            afn = ExpresionRegular(regex).convertir_a_afn()
            modelos = [afn, afn.convertir_a_afd(), afn.minimizar_afd(),
                       afn.convertir_a_afd().minimizar_afd()]
            for cadena in cadenas(alfabeto, 4):
                esperado = re.fullmatch(regex.replace('ε', '').replace('e', ''), cadena) is not None
                for modelo in modelos:
                    with self.subTest(regex=regex, cadena=cadena):
                        self.assertEqual(modelo.simular(cadena), esperado)
                        self.comprobaciones += 1
        print('Comparaciones con expresiones regulares:', self.comprobaciones)

    def test_entradas_invalidas(self):
        for regex in ['', '(', 'a)', '()', '*a', 'a|', '|a', 'a||b', 'a·b']:
            with self.subTest(regex=regex), self.assertRaises(ValueError):
                ExpresionRegular(regex)
        for operacion in ['simular', 'convertir_a_afd', 'minimizar_afd']:
            with self.assertRaises(ValueError):
                getattr(Automata(), operacion)(*([''] if operacion == 'simular' else []))

    def test_epsilon(self):
        for regex in ['e', 'ε']:
            a = ExpresionRegular(regex).convertir_a_afn()
            self.assertTrue(a.simular(''))
            self.assertFalse(a.simular('e'))
            self.assertFalse(a.simular('ε'))
        a = Automata()
        for q in ['q0', 'q1']: a.agregar_estado(q)
        a.definir_inicial('q0'); a.agregar_final('q1')
        a.agregar_transicion('q0', 'ε', 'q1')
        self.assertTrue(a.simular(''))
        with self.assertRaises(ValueError): a.agregar_simbolo('e')

    def test_minimo_y_alfabeto(self):
        a = Automata()
        for q in ['s', 'p', 'q']: a.agregar_estado(q)
        for s in 'ab': a.agregar_simbolo(s)
        a.definir_inicial('s')
        a.agregar_transicion('s', 'a', 'p')
        a.agregar_transicion('s', 'b', 'q')
        a.agregar_transicion('p', 'a', 'p')
        self.assertEqual(len(a.minimizar_afd().estados), 1)
        self.assertEqual(a.tabla_distinguibilidad(), set())
        self.assertEqual(a.convertir_a_afd().alfabeto, set('ab'))
        self.assertEqual(len(ExpresionRegular('(0|1)*01').convertir_a_afn().minimizar_afd().estados), 3)

    def test_afn_aleatorios(self):
        rng = random.Random(42)
        total = 0
        for _ in range(80):
            a = Automata()
            for q in ['q0', 'q1', 'q2', 'q3']: a.agregar_estado(q)
            for s in 'ab': a.agregar_simbolo(s)
            a.definir_inicial('q0')
            for q in sorted(a.estados):
                if rng.random() < .4: a.agregar_final(q)
                for s in ['a', 'b', 'e']:
                    for destino in sorted(a.estados):
                        if rng.random() < .15: a.agregar_transicion(q, s, destino)
            d, m = a.convertir_a_afd(), a.minimizar_afd()
            self.assertTrue(d.es_determinista())
            self.assertTrue(m.es_determinista())
            self.assertEqual(m.alfabeto, a.alfabeto)
            # Un AFD mínimo tiene todos sus pares de estados distinguibles.
            n = len(m.estados)
            self.assertEqual(len(m.tabla_distinguibilidad()), n * (n - 1) // 2)
            for cadena in cadenas('ab', 5):
                self.assertEqual(a.simular(cadena), d.simular(cadena))
                self.assertEqual(a.simular(cadena), m.simular(cadena))
                total += 2
        print('Comparaciones de AFN aleatorios:', total)


if __name__ == '__main__':
    unittest.main(verbosity=2)
