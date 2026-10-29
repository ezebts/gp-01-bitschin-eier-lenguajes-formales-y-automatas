import sys
import ast
import copy
from pathlib import Path
from logging import getLogger
from dataclasses import dataclass
from collections.abc import Iterator


logger = getLogger(__name__)


@dataclass
class Funcion:
    """ Representa una función de un archivo Python. """

    nombre: str
    archivo: str
    linea: int

    AST: ast.AST
    AST_NORMALIZADO: ast.AST = None
    AST_NORMALIZADO_NODOS: list[ast.AST] = None

    def __post_init__(self):
        self.AST_NORMALIZADO_NODOS = []
        for nodo in recorrer_en_preorder(copy.deepcopy(self.AST)):
            nodo_normalizado = self._normalizar_nodo_funcion(nodo)
            self.AST_NORMALIZADO_NODOS.append(nodo_normalizado)
        self.AST_NORMALIZADO = self.AST_NORMALIZADO_NODOS[0]

    def _normalizar_nodo_funcion(cls, nodo: ast.AST) -> ast.AST:
        return type(nodo) # TODO: Implementar


def extraer_funciones(directorio) -> Iterator[Funcion]:
    
    for path in Path(directorio).rglob("*.py"):
        
        try:
            arbol = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.warning(f"Error al parsear el archivo '{path}': {e}")
            continue
        
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield Funcion(
                    nombre=nodo.name,
                    archivo=str(path),
                    linea=nodo.lineno,
                    AST=nodo
                )


def recorrer_en_preorder(AST: ast.AST) -> Iterator[ast.AST]:
    yield AST
    for hijo in ast.iter_child_nodes(AST):
        yield from recorrer_en_preorder(hijo)


def ngramas(secuencia, n) -> set:
    ngramas = []
    for i in range(len(secuencia) - n + 1):
        ngramas.append(tuple(secuencia[i:i+n]))
    return set(ngramas)

def jacad(secuencia_a, secuencia_b, n) -> float:

    ngramas_a = ngramas(secuencia_a, n)
    ngramas_b = ngramas(secuencia_b, n)

    if not ngramas_a and not ngramas_b:
        return 1.0

    ngramas_totales = ngramas_a.union(ngramas_b)
    ngramas_coincidentes = ngramas_a.intersection(ngramas_b)

    return len(ngramas_coincidentes) / len(ngramas_totales)


def dibujar_arbolito(AST, prefijo="", es_ultimo=True, es_raiz=True):

    nombre = type(AST).__name__

    if es_raiz:
        print(nombre)
        prefijo_hijos = ""
    else:
        rama = "└── " if es_ultimo else "├── "
        print(prefijo + rama + nombre)
        prefijo_hijos = prefijo + ("    " if es_ultimo else "│   ")

    hijos = list(ast.iter_child_nodes(AST))
    for i, hijo in enumerate(hijos):
        dibujar_arbolito(hijo, prefijo_hijos, i == len(hijos) - 1, es_raiz=False)


if __name__ == "__main__":
    
    path_directorio = sys.argv[1]
    
    funcion_saludar, funcion_despedir, *_ = extraer_funciones(path_directorio)
    
    print("\nFuncion saludar:")
    dibujar_arbolito(funcion_saludar.AST)
    print("\nPreorder: ", funcion_saludar.AST_NORMALIZADO_NODOS)
    
    print("\nFuncion despedir:")
    dibujar_arbolito(funcion_despedir.AST)
    print("\nPreorder: ", funcion_despedir.AST_NORMALIZADO_NODOS)
    print("\n" )
    
    similitud = jacad(funcion_saludar.AST_NORMALIZADO_NODOS, funcion_despedir.AST_NORMALIZADO_NODOS, n=3)
    print(f"{similitud * 100:.2f}% de similitud")
    print("")
