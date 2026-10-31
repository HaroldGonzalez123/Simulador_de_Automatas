import unittest
from logs import validar_linea, validar_logs, EJEMPLO_LOGS

class PruebasLogs(unittest.TestCase):
    def test_niveles(self):
        for nivel in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            self.assertTrue(validar_linea(f'2026-10-31 08:00:00 [{nivel}] Mensaje de prueba')[0])

    def test_fechas_y_horas(self):
        self.assertTrue(validar_linea('2024-02-29 23:59:59 [INFO] Año bisiesto')[0])
        for fecha in ['2026-02-29', '2026-02-30', '2026-13-01', '0000-01-01']:
            self.assertFalse(validar_linea(f'{fecha} 08:00:00 [INFO] Mensaje')[0])
        for hora in ['24:00:00', '12:60:00', '12:00:60']:
            self.assertFalse(validar_linea(f'2026-10-31 {hora} [INFO] Mensaje')[0])

    def test_formato_invalido(self):
        for linea in ['', 'texto', '2026-10-31 08:00:00 [INFO] ',
                      '2026-10-31 08:00:00 [INFO]   ',
                      '2026-10-31 08:00:00 [info] Mensaje',
                      '2026-10-31 08:00:00 [OTRO] Mensaje',
                      '2026-1-1 08:00:00 [INFO] Mensaje']:
            self.assertFalse(validar_linea(linea)[0])

    def test_ejemplo_y_numeracion(self):
        resultados = validar_logs(EJEMPLO_LOGS)
        self.assertEqual(len(resultados), 7)
        self.assertEqual(sum(r['valido'] for r in resultados), 3)
        resultados = validar_logs('\r\n2026-10-31 08:00:00 [INFO] Mensaje\r\n\r\nIncorrecto')
        self.assertEqual([r['linea'] for r in resultados], [2, 4])
        self.assertEqual(validar_logs(' \n\t\n'), [])
        with self.assertRaises(ValueError): validar_logs(None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
