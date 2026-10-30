import ast
import argparse

from buscar_similares.extraccion import Funcion, cargar_funcion
from buscar_similares.almacenamiento import cargar_por_similitud


N_GRAMAS = 3
UMBRAL_DUPLICADO = 0.7


def crear_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description="Busca funciones similares comparando sus AST normalizados.")
    parser.add_argument("--dir", required=True, help="carpeta con los archivos .py donde buscar")

    objetivo = parser.add_mutually_exclusive_group(required=True)
    objetivo.add_argument("--funcion", help="función objetivo como ARCHIVO.py:FUNCION, ej: prueba.py:saludar")
    objetivo.add_argument("--codigo", help="código de la función objetivo, pegado entre comillas")

    parser.add_argument("--top", type=int, default=5, help="cantidad de resultados (default: 5)")
    return parser


def main_cli():

    parser = crear_parser()
    args = parser.parse_args()

    if args.funcion:
        objetivo = cargar_funcion(args.dir, args.funcion) if ":" in args.funcion else None
        if objetivo is None:
            parser.error(f"no se encontró la función '{args.funcion}' (formato: ARCHIVO.py:FUNCION)")
    else:
        nodo = ast.parse(args.codigo).body[0]
        if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parser.error("el código pegado tiene que empezar con una función (def ...)")
        objetivo = Funcion(nombre=nodo.name, archivo="<pegado>", linea=nodo.lineno, AST=nodo)

    funciones, similitudes = cargar_por_similitud(args.dir, objetivo, N_GRAMAS)

    print(f"Función objetivo: {objetivo.nombre} ({objetivo.archivo}:{objetivo.linea})\n")
    print(f"{'#':>3}  {'Score':>6}  {'¿Duplicado?':<11}  Ubicación")
    for posicion, (funcion, similitud) in enumerate(zip(funciones[:args.top], similitudes[:args.top]), start=1):
        duplicado = "SÍ" if similitud >= UMBRAL_DUPLICADO else "no"
        print(f"{posicion:>3}  {similitud:>6.3f}  {duplicado:<11}  {funcion.archivo}:{funcion.linea}  {funcion.nombre}")
