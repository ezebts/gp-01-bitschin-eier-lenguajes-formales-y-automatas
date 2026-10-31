import ast
import builtins


def quitar_docstring(nodo: ast.FunctionDef | ast.AsyncFunctionDef):
    cuerpo = nodo.body
    if (cuerpo
            and isinstance(cuerpo[0], ast.Expr)
            and isinstance(cuerpo[0].value, ast.Constant)
            and isinstance(cuerpo[0].value.value, str)):
        nodo.body = cuerpo[1:] or [ast.Pass()]


def normalizar_variable(nombre_variable: str, mapa_variables: dict[str, str]) -> str:

    if nombre_variable not in mapa_variables:
        variables_totales = len(mapa_variables)
        mapa_variables[nombre_variable] = f"VAR{variables_totales + 1}"

    return mapa_variables[nombre_variable]


def normalizar_nodo_funcion(nodo: ast.AST, mapa_variables: dict[str, str]) -> list[str]:

    tokens_normalizados: list[str] = []

    if isinstance(nodo, ast.FunctionDef | ast.AsyncFunctionDef):
        nodo.name = "_"
        quitar_docstring(nodo)
        tokens_normalizados.append(nodo.name)

    elif isinstance(nodo, ast.arg):
        nodo.arg = normalizar_variable(nodo.arg, mapa_variables)
        tokens_normalizados.append(nodo.arg)

    elif isinstance(nodo, ast.Name):
        lectura_builtin = (
            isinstance(nodo.ctx, ast.Load)
            and nodo.id in vars(builtins)
            and nodo.id not in mapa_variables
        )
        if not lectura_builtin:
            nodo.id = normalizar_variable(nodo.id, mapa_variables)
        tokens_normalizados.append(nodo.id)

    elif isinstance(nodo, ast.Constant):
        nodo.value = "LIT"
        tokens_normalizados.append(nodo.value)

    return tokens_normalizados
