from collections import Counter
from decimal import Decimal, getcontext

# Zwiększ precyzję dla operacji na liczbach typu Decimal
# Musi mieć około 2500, żeby poprawnie zakodować i odkodować krótki tekst
getcontext().prec = 50

def calculate_probabilities(message):
    total_count = len(message)
    symbol_counts = Counter(message)
    return {symbol: Decimal(count) / Decimal(total_count) for symbol, count in symbol_counts.items()}

def precompute_cumulative_probs(symbols_with_probs):
    # Oblicz prawdopodobieństwa skumulowane dla symboli
    cumulative_probs = {}
    cumulative = Decimal(0)
    for symbol, prob in sorted(symbols_with_probs.items()):
        cumulative_probs[symbol] = (cumulative, cumulative + prob)
        cumulative += prob
    return cumulative_probs

def arithmetic_encode(message):
    # Oblicz prawdopodobieństwa symboli
    symbols_with_probs = calculate_probabilities(message)
    
    # Oblicz z wyprzedzeniem prawdopodobieństwa skumulowane
    cumulative_probs = precompute_cumulative_probs(symbols_with_probs)

    low = Decimal(0)
    high = Decimal(1)

    # Wykonaj kodowanie arytmetyczne
    for symbol in message:
        range_width = high - low
        symbol_low, symbol_high = cumulative_probs[symbol]
        high = low + range_width * symbol_high
        low = low + range_width * symbol_low

    # Zwróć punkt środkowy zakresu, aby uniknąć problemów z precyzją
    return (low + high) / 2, symbols_with_probs

def arithmetic_decode(encoded_value, message_length, symbols_with_probs):
    # Oblicz z wyprzedzeniem prawdopodobieństwa skumulowane
    cumulative_probs = precompute_cumulative_probs(symbols_with_probs)

    decoded_message = []
    for _ in range(message_length):
        for symbol, (symbol_low, symbol_high) in cumulative_probs.items():
            if symbol_low <= encoded_value < symbol_high:
                decoded_message.append(symbol)
                range_width = symbol_high - symbol_low
                # Zaktualizuj encoded_value: znormalizuj je w zakresie symbolu
                encoded_value = (encoded_value - symbol_low) / range_width
                break

    return ''.join(decoded_message)
