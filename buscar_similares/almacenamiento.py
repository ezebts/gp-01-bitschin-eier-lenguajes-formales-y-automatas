from buscar_similares.extraccion import Funcion, extraer_funciones
from buscar_similares.similitud import jacad


def cargar_funciones(directorio) -> dict[str, Funcion]:
    return {funcion.identificador: funcion for funcion in extraer_funciones(directorio)}


def ordenar_por_similitud(funciones: dict[str, Funcion], objetivo: Funcion, n: int = 3) -> dict[str, float]:

    similitudes = {}
    for identificador, funcion in funciones.items():
        if identificador != objetivo.identificador:
            similitudes[identificador] = jacad(objetivo.AST_NORMALIZADO_TOKENS, funcion.AST_NORMALIZADO_TOKENS, n)

    return dict(sorted(similitudes.items(), key=lambda item: item[1], reverse=True))
