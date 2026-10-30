import sys

from buscar_similares import similitud
from buscar_similares.extraccion import extraer_funciones
from buscar_similares.visualizacion import dibujar_arbolito


def main_cli():

    path_directorio = sys.argv[1]

    funcion_saludar, funcion_despedir, *_ = extraer_funciones(path_directorio)

    print(f"\nFuncion {funcion_saludar.identificador}:")
    dibujar_arbolito(funcion_saludar.AST_NORMALIZADO)
    print("\nPreorder: ", funcion_saludar.AST_NORMALIZADO_TOKENS)

    print(f"\nFuncion {funcion_despedir.identificador}:")
    dibujar_arbolito(funcion_despedir.AST_NORMALIZADO)
    print("\nPreorder: ", funcion_despedir.AST_NORMALIZADO_TOKENS)
    print("\n" )

    puntuacion = similitud.jacad(funcion_saludar.AST_NORMALIZADO_TOKENS, funcion_despedir.AST_NORMALIZADO_TOKENS, n=3)
    print(f"{puntuacion * 100:.2f}% de similitud")
    print("")
