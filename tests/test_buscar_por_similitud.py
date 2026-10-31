import unittest
from pathlib import Path

from buscar_similares.extraccion import cargar_funcion, cargar_funcion_desde_directorio
from buscar_similares.busqueda import buscar_por_similitud


EJEMPLOS = Path(__file__).parent / "ejemplos"


def buscar(carpeta, identificador):
    directorio = EJEMPLOS / carpeta
    objetivo = cargar_funcion_desde_directorio(directorio, identificador)
    return buscar_por_similitud(directorio, objetivo)


def get_coincidencia(coincidencias, nombre):
    encontradas = [c for c in coincidencias if c.funcion.nombre == nombre]
    assert encontradas, f"Se esperaba '{nombre}' como coincidencia."
    return encontradas[0]


class TestBuscarPorSimilitud(unittest.TestCase):

    def test_renombre_es_duplicado(self):
        coincidencias = buscar("renombre", "pares.py:sumar")
        agregar = get_coincidencia(coincidencias, "agregar")
        self.assertEqual(agregar.similitud, 1.0)
        self.assertTrue(agregar.es_duplicado)
        self.assertEqual(coincidencias[0].funcion.nombre, "agregar")

    def test_literales_distintos_es_duplicado(self):
        coincidencias = buscar("directorio_simple", "prueba.py:saludar")
        despedir = get_coincidencia(coincidencias, "despedir")
        self.assertEqual(despedir.similitud, 1.0)
        self.assertTrue(despedir.es_duplicado)

    def test_docstring_no_cambia_similitud(self):
        coincidencias = buscar("docstring", "pares.py:con_doc")
        sin_doc = get_coincidencia(coincidencias, "sin_doc")
        self.assertEqual(sin_doc.similitud, 1.0)
        self.assertTrue(sin_doc.es_duplicado)

    def test_estructura_distinta_no_es_duplicado(self):
        coincidencias = buscar("estructura_distinta", "pares.py:sumar")
        maximo = get_coincidencia(coincidencias, "maximo")
        self.assertFalse(maximo.es_duplicado)

    def test_dominios_distintos_no_es_duplicado(self):
        coincidencias = buscar("dominios_distintos", "pares.py:factorial")
        parsear = get_coincidencia(coincidencias, "parsear_enteros")
        self.assertFalse(parsear.es_duplicado)

    def test_clon_reordenado_es_duplicado(self):
        coincidencias = buscar("reordenado", "pares.py:ordenar_ambas")
        reordenado = get_coincidencia(coincidencias, "ordenar_ambas_v2")
        self.assertEqual(reordenado.similitud, 1.0)
        self.assertTrue(reordenado.es_duplicado)
        self.assertEqual(coincidencias[0].funcion.nombre, "ordenar_ambas_v2")

    def test_no_incluye_el_objetivo(self):
        coincidencias = buscar("renombre", "pares.py:sumar")
        nombres = [c.funcion.nombre for c in coincidencias]
        self.assertNotIn("sumar", nombres)

    def test_archivo_roto_no_rompe_la_busqueda(self):
        directorio = EJEMPLOS / "archivo_roto"
        objetivo = cargar_funcion("def identidad(x):\n    return x\n")
        coincidencias = buscar_por_similitud(directorio, objetivo)
        identidad = get_coincidencia(coincidencias, "identidad")
        self.assertEqual(identidad.similitud, 1.0)

    def test_codigo_pegado_encuentra_el_clone(self):
        directorio = EJEMPLOS / "renombre"
        objetivo = cargar_funcion("def sumar(x, y):\n    return x + y\n")
        coincidencias = buscar_por_similitud(directorio, objetivo)
        agregar = get_coincidencia(coincidencias, "agregar")
        self.assertEqual(agregar.similitud, 1.0)
        self.assertTrue(agregar.es_duplicado)


if __name__ == "__main__":
    unittest.main()
