from collections import Counter
import math


def calculate_entropy(text):
    # Zliczanie częstotliwości występowania znaków
    freq = Counter(text)
    total = len(text)  # Długość tekstu
    
    # Obliczanie entropii
    entropy = -sum((count / total) * math.log2(count / total) for count in freq.values())
    return entropy