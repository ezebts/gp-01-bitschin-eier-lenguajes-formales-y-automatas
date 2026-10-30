from bisect import bisect

from buscar_similares.extraccion import Funcion, extraer_funciones
from buscar_similares.similitud import jacad


def cargar_por_similitud(directorio, objetivo: Funcion, n: int = 3) -> tuple[list[Funcion], list[float]]:

    funciones = []
    indice = []

    for funcion in extraer_funciones(directorio):

        if funcion.identificador == objetivo.identificador:
            continue

        similitud = jacad(objetivo.AST_NORMALIZADO_TOKENS, funcion.AST_NORMALIZADO_TOKENS, n)

        pos = bisect(indice, similitud)

        funciones.insert(pos, funcion)
        indice.insert(pos, similitud)

    # bisect ordena de menor a mayor: se dan vuelta para que la más similar quede primera
    return funciones[::-1], indice[::-1]
