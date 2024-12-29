import math
from collections import Counter

# Budowa tabeli symboli dla tANS
def build_tans_table(data, table_size=256):
    frequencies = Counter(data)
    total = sum(frequencies.values())
    probabilities = {k: v / total for k, v in frequencies.items()}

    table = []
    for symbol, prob in probabilities.items():
        count = int(prob * table_size)
        table.extend([symbol] * count)

    unique_chars = set(data)
    while len(table) < table_size:
        table.extend(unique_chars)  # Dodajemy brakujące znaki
    return table[:table_size]

# Kodowanie tANS
def tans_encode(data, table):
    state = 1  # Początkowy stan
    encoded = []

    for char in data:
        if char not in table:  # Sprawdzenie, czy znak istnieje w tabeli
            table.append(char)  # Dodanie brakującego znaku
        index = table.index(char)
        encoded.append(state % len(table))
        state = (state // len(table)) * len(table) + index

    return state, encoded

# Dekodowanie tANS
def tans_decode(encoded, state, table):
    decoded = []
    table_size = len(table)

    while encoded:
        symbol_index = state % table_size
        state = (state // table_size) * table_size + encoded.pop()
        decoded.append(table[symbol_index])

    return ''.join(decoded[::-1])

# Testowanie kodowania tANS
def test_tans(text):
    table = build_tans_table(text)
    
    print("Tabela tANS:", table)

    # Kodowanie
    state, encoded = tans_encode(text, table)
    print("Zakodowany stan:", state)
    print("Zakodowane dane:", encoded)

    # Dekodowanie
    decoded = tans_decode(encoded, state, table)
    print("Odkodowany tekst:", decoded)

    # Sprawdzenie poprawności
    assert text == decoded, "Odkodowany tekst nie zgadza się z oryginałem!"
