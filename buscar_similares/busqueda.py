from bisect import bisect

from buscar_similares.extraccion import Funcion, extraer_funciones
from buscar_similares.similitud import jacad


def buscar_por_similitud(directorio, objetivo: Funcion, n: int = 3) -> list[tuple[float, Funcion]]:

    resultados = []

    for funcion in extraer_funciones(directorio):

        if funcion.identificador == objetivo.identificador:
            continue

        similitud = jacad(objetivo.AST_NORMALIZADO_TOKENS, funcion.AST_NORMALIZADO_TOKENS, n)

        # bisect ordena de menor a mayor: con -similitud la más similar queda primera
        pos = bisect(resultados, -similitud, key=lambda match: -match[0])
        resultados.insert(pos, (similitud, funcion))

    return resultados
