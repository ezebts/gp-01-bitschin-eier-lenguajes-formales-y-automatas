import ast
import copy
from pathlib import Path
from logging import getLogger
from dataclasses import dataclass
from collections.abc import Iterator

from buscar_similares.busqueda import recorrer_en_preorder
from buscar_similares.normalizacion import normalizar_nodo_funcion


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
            tokens_normalizados = normalizar_nodo_funcion(nodo, self._mapa_variables)
            self.AST_NORMALIZADO_TOKENS.append(type(nodo).__name__)
            self.AST_NORMALIZADO_TOKENS.extend(tokens_normalizados)


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
