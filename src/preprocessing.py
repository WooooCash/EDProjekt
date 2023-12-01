from statistics import mean, stdev

"""
Columnar operation function structure:

Inputs:
    column: list
    config: dict of parameters which will be required for the operation 

Output:
    column: list

Przykładowo:
def operacja(column: list, config: dict) -> list:
    '''Tu w komentarzu (trzy ciapki ' albo ") można podać co przyjmujemy w konfigu (pokaże się w podpowiedziach autocomplete)'''
    
    modified_col = [] <-- najlepiej tworzyć nową listę do której wrzucamy zmienione dane aby nie mutować oryginalnej kolumny w międzyczasie
    jakaś logika przetwarzająca
    return modified_col

---

Narazie trzymajmy wszystkie funkcje w jednym pliku (albo dwóch dopóki pracujemy jednocześnie).

Jeśli wyjdzie na to że niektóre operacje będą dosyć skomplikowane i będą potrzebować kilka funkcji pomocniczych
to sobie wydzielimy katalog src/preprocessing/ w którym każda operacja będzie w swoim pliku
"""


def to_numeric(column: list, config: dict) -> list[int]:
    """
    column: list of string values
    config: empty
    """
    if type(column[0]) == int:
        return column

    modified_col = []
    mapping: dict[str, int] = {}

    for value in column:
        numeric_val = mapping.get(value)
        if numeric_val is None:
            numeric_val = len(mapping)
            mapping[value] = numeric_val

        modified_col.append(numeric_val)

    return modified_col


def standardize(column: list[float], config: dict) -> list:
    """
    column: list of floating point values
    config: empty
    """

    modified_col = []

    col_mean = mean(column)
    col_stdev = stdev(column)

    for value in column:
        new_val = (value - col_mean) / col_stdev
        modified_col.append(round(new_val, 3))

    return modified_col
