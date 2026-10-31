from bisect import bisect
from dataclasses import dataclass

from buscar_similares.extraccion import Funcion, extraer_funciones
from buscar_similares.similitud import jacad


UMBRAL_DUPLICADO = 0.7


@dataclass
class Coincidencia:
    funcion: Funcion
    similitud: float

    @property
    def es_duplicado(self) -> bool:
        return self.similitud >= UMBRAL_DUPLICADO


def buscar_por_similitud(directorio, objetivo: Funcion, ngramas: int = 3, topk: int = 5) -> list[Coincidencia]:

    coincidencias = []

    for funcion in extraer_funciones(directorio):

        if funcion.identificador == objetivo.identificador:
            continue

        similitud = jacad(objetivo.AST_NORMALIZADO_TOKENS, funcion.AST_NORMALIZADO_TOKENS, ngramas)
        coincidencia = Coincidencia(funcion, similitud)

        # bisect ordena de menor a mayor: con -similitud la más similar queda primera
        pos = bisect(coincidencias, -similitud, key=lambda match: -match.similitud)
        coincidencias.insert(pos, coincidencia)
        coincidencias = coincidencias[:topk]

    return coincidencias
