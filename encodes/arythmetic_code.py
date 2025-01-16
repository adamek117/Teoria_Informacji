from collections import Counter
from decimal import Decimal, getcontext
import time

# Zwiększ precyzję dla operacji na liczbach typu Decimal
# Musi mieć około 2500, żeby poprawnie zakodować i odkodować krótki tekst
getcontext().prec = 2500

def split_message(message, segment_length):
    return [message[i:i+segment_length] for i in range(0, len(message), segment_length)]

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
                encoded_value = max(min((encoded_value - symbol_low) / range_width, Decimal(1)), Decimal(0))
                break
        else:
            print(f"Error: Encoded value {encoded_value} did not match any range.")
            break

    return ''.join(decoded_message)

def arithmetic_encode_large(message, segment_length=500):
    segments = split_message(message, segment_length)
    encoded_segments = []
    all_symbols_with_probs = []
    for segment in segments:
        encoded_value, symbols_with_probs = arithmetic_encode(segment)
        encoded_segments.append(encoded_value)
        all_symbols_with_probs.append(symbols_with_probs)
    return encoded_segments, all_symbols_with_probs

def arithmetic_decode_large(encoded_segments, segment_length, all_symbols_with_probs):
    decoded_message = []
    for encoded_value, symbols_with_probs in zip(encoded_segments, all_symbols_with_probs):
        segment = arithmetic_decode(encoded_value, segment_length, symbols_with_probs)
        decoded_message.append(segment)
    return ''.join(decoded_message)

if __name__ == '__main__':
    with open("../data/full/MalyKsiaze/English.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    start = time.time()
    encoded_segments, all_probs = arithmetic_encode_large(large_text, segment_length=1500)
    print(f"Encoding time: {time.time() - start:.2f} s")
    decoded_text = arithmetic_decode_large(encoded_segments, 1500, all_probs)

    with open("../data/full/MalyKsiaze/English_decoded.txt", "w", encoding="utf-8") as file:
        file.write(decoded_text)
