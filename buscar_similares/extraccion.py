import ast
import copy
from pathlib import Path
from logging import getLogger
from dataclasses import dataclass
from collections.abc import Iterator

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


def recorrer_en_preorder(AST: ast.AST) -> Iterator[ast.AST]:
    yield AST
    for hijo in ast.iter_child_nodes(AST):
        yield from recorrer_en_preorder(hijo)


def extraer_funciones(directorio) -> Iterator[Funcion]:

    directorio = Path(directorio)

    for path in directorio.rglob("*.py"):
        yield from _extraer_funciones_archivo(path, directorio)


def cargar_funcion(directorio, identificador: str) -> Funcion | None:

    directorio = Path(directorio)
    path_archivo, nombre = identificador.rsplit(":", 1)

    for funcion in _extraer_funciones_archivo(directorio / path_archivo, directorio):
        if funcion.nombre == nombre:
            return funcion
    return None


def _extraer_funciones_archivo(path: Path, directorio: Path) -> Iterator[Funcion]:

    try:
        arbol = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError) as e:
        logger.warning(f"Error al parsear el archivo '{path}': {e}")
        return

    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield Funcion(
                nombre=nodo.name,
                archivo=str(path.relative_to(directorio)),
                linea=nodo.lineno,
                AST=nodo
            )
