
def _ngramas(secuencia, n) -> set:
    ngramas = []
    for i in range(len(secuencia) - n + 1):
        ngramas.append(tuple(secuencia[i:i+n]))
    return set(ngramas)


def jacad(secuencia_a, secuencia_b, n) -> float:

    ngramas_a = _ngramas(secuencia_a, n)
    ngramas_b = _ngramas(secuencia_b, n)

    if not ngramas_a and not ngramas_b:
        return 1.0

    ngramas_totales = ngramas_a.union(ngramas_b)
    ngramas_coincidentes = ngramas_a.intersection(ngramas_b)

    return len(ngramas_coincidentes) / len(ngramas_totales)
