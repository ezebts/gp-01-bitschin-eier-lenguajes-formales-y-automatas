import ast


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
