def factorial(n):
    r = 1
    for i in range(n):
        r = r * (i + 1)
    return r


def parsear_enteros(texto):
    partes = texto.split(",")
    return [int(p) for p in partes]
