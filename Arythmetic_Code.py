from collections import defaultdict

def arithmetic_encode(text):
    # Oblicz częstotliwości symboli w tekście
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1
    
    total_symbols = len(text)
    probabilities = {char: freq[char] / total_symbols for char in freq}

    # Inicjalizuj zakres
    low, high = 0.0, 1.0

    # Kodowanie
    for char in text:
        range_size = high - low
        high = low + range_size * sum(probabilities[c] for c in sorted(probabilities.keys()) if c < char)
        low = low + range_size * sum(probabilities[c] for c in sorted(probabilities.keys()) if c <= char)

    return (low + high) / 2
