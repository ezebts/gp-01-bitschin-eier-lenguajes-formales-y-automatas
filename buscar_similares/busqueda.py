import ast
from collections.abc import Iterator


def recorrer_en_preorder(AST: ast.AST) -> Iterator[ast.AST]:
    yield AST
    for hijo in ast.iter_child_nodes(AST):
        yield from recorrer_en_preorder(hijo)
