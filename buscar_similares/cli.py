import argparse

from buscar_similares.extraccion import cargar_funcion, cargar_funcion_desde_directorio
from buscar_similares.busqueda import buscar_por_similitud


def crear_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser("buscar_similares", description="Busca funciones similares comparando sus AST normalizados.")
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
        objetivo = cargar_funcion_desde_directorio(args.dir, args.funcion)
        if objetivo is None:
            parser.error(f"no se encontró la función '{args.funcion}' (formato: ARCHIVO.py:FUNCION)")
    else:
        objetivo = cargar_funcion(args.codigo)
        if objetivo is None:
            parser.error("el código pegado tiene que empezar con una función (def ...)")

    coincidencias = buscar_por_similitud(args.dir, objetivo, topk=args.top)

    print(f"Función objetivo: {objetivo.nombre} ({objetivo.archivo}:{objetivo.linea})\n")
    print(f"{'#':>3}  {'Score':>6}  {'¿Duplicado?':<11}  Ubicación")
    for posicion, coincidencia in enumerate(coincidencias, start=1):
        funcion = coincidencia.funcion
        duplicado = "Si" if coincidencia.es_duplicado else "No"
        print(f"{posicion:>3}  {coincidencia.similitud:>6.3f}  {duplicado:<11}  {funcion.archivo}:{funcion.linea}  {funcion.nombre}")
