import sys
import ast
import copy
import builtins
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
    AST_NORMALIZADO_TOKENS: list[str] = None

    @property
    def identificador(self) -> str:
        return f"{self.archivo}:{self.nombre}"

    def __post_init__(self):
        self._mapa_variables = {}
        self.AST_NORMALIZADO_TOKENS = []
        self.AST_NORMALIZADO = copy.deepcopy(self.AST)
        for nodo in recorrer_en_preorder(self.AST_NORMALIZADO):
            tokens_normalizados = self._normalizar_nodo_funcion(nodo)
            self.AST_NORMALIZADO_TOKENS.append(type(nodo).__name__)
            self.AST_NORMALIZADO_TOKENS.extend(tokens_normalizados)

    def _quitar_docstring(self, nodo: ast.FunctionDef | ast.AsyncFunctionDef):
        cuerpo = nodo.body
        if (cuerpo
                and isinstance(cuerpo[0], ast.Expr)
                and isinstance(cuerpo[0].value, ast.Constant)
                and isinstance(cuerpo[0].value.value, str)):
            nodo.body = cuerpo[1:] or [ast.Pass()]

    def _normalizar_variable(self, nombre_variable: str) -> str:
        
        if nombre_variable not in self._mapa_variables:
            variables_totales = len(self._mapa_variables)
            self._mapa_variables[nombre_variable] = f"VAR{variables_totales + 1}"
        
        return self._mapa_variables[nombre_variable]

    def _normalizar_nodo_funcion(cls, nodo: ast.AST) -> list[str]:
        
        tokens_normalizados: list[str] = []
        
        if isinstance(nodo, ast.FunctionDef | ast.AsyncFunctionDef):
            nodo.name = "_"
            cls._quitar_docstring(nodo)
            tokens_normalizados.append(nodo.name)
        
        elif isinstance(nodo, ast.arg):
            nodo.arg = cls._normalizar_variable(nodo.arg)
            tokens_normalizados.append(nodo.arg)
        
        elif isinstance(nodo, ast.Name):
            nodo.id = cls._normalizar_variable(nodo.id)
            tokens_normalizados.append(nodo.id)
        
        elif isinstance(nodo, ast.Constant):
            nodo.value = "LIT"
            tokens_normalizados.append(nodo.value)
        
        return tokens_normalizados


def extraer_funciones(directorio) -> Iterator[Funcion]:

    directorio = Path(directorio)

    for path in directorio.rglob("*.py"):
        
        try:
            arbol = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.warning(f"Error al parsear el archivo '{path}': {e}")
            continue
        
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield Funcion(
                    nombre=nodo.name,
                    archivo=str(path.relative_to(directorio)),
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
    nombre_opciones = ("id", "arg", "value", "name")
    for opcion in nombre_opciones:
        atributo = getattr(AST, opcion, None)
        if isinstance(atributo, str):
            nombre = type(AST).__name__ + ": " + atributo
            break

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
    
    print(f"\nFuncion {funcion_saludar.identificador}:")
    dibujar_arbolito(funcion_saludar.AST_NORMALIZADO)
    print("\nPreorder: ", funcion_saludar.AST_NORMALIZADO_TOKENS)
    
    print(f"\nFuncion {funcion_despedir.identificador}:")
    dibujar_arbolito(funcion_despedir.AST_NORMALIZADO)
    print("\nPreorder: ", funcion_despedir.AST_NORMALIZADO_TOKENS)
    print("\n" )
    
    similitud = jacad(funcion_saludar.AST_NORMALIZADO_TOKENS, funcion_despedir.AST_NORMALIZADO_TOKENS, n=3)
    print(f"{similitud * 100:.2f}% de similitud")
    print("")
