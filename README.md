
Uso:

- `python -m buscar_similares -h`
- `python -m buscar_similares --dir ./tests/ejemplos/directorio_simple --funcion prueba.py:saludar --top 5`
- `python -m buscar_similares --dir ./tests/ejemplos/directorio_simple --codigo "def f(m): return 'hola ' + m"`

Tests:

- `python -m unittest discover -s tests`
