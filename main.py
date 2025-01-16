import os
import struct
import pandas as pd

from encodes.ans import tans_encode, tans_decode, build_tans_table
from encodes.arythmetic_code import arithmetic_encode_large, arithmetic_decode_large
from encodes.huffman_code import huffman_encode, huffman_decode
from read_file import read_text_from_file
from performance_tests.test_compression import compression_ratio
from performance_tests.test_entropy import calculate_entropy
from performance_tests.test_measure_cpu_usage import measure_cpu_usage
from performance_tests.test_memory_usage import test_memory_usage_func
from performance_tests.test_stability import stability_test
from performance_tests.text_execution_time import test_execution_time_func


def ensure_results_dir():
    os.makedirs("results", exist_ok=True)

# Funkcja do zapisywania wyników do pliku
def save_results_to_file(filename, results):
    ensure_results_dir()
    with open(os.path.join("results", filename), "w") as file:
        for key, value in results.items():
            if key in ["Original Size", "Huffman CPU Usage", "Arithmetic CPU Usage"]:
                file.write(f"{key}: {value}\n")
                file.write(50 * "-" + "\n")
            else:
                file.write(f"{key}: {value}\n")

if __name__ == '__main__':
    """Dane wejściowe"""
    # Pełne teksty Małego Księcia w różnych językach
    texts_full = {
        "English - Full Text": read_text_from_file('data/full/MalyKsiaze/English.txt'),
        "French - Full Text": read_text_from_file('data/full/MalyKsiaze/French.txt'),
        "Hungary - Full Text": read_text_from_file('data/full/MalyKsiaze/Hungary.txt'),
        "Polish - Full Text": read_text_from_file('data/full/MalyKsiaze/Polish.txt')
    }

    # Pierwszy oraz Drugi rozdział Małego Księcia w różnych językach
    texts_short = {
        "English": read_text_from_file('data/short/MalyKsiaze/English.txt'),
        "French": read_text_from_file('data/short/MalyKsiaze/French.txt'),
        "Hungary": read_text_from_file('data/short/MalyKsiaze/Hungary.txt'),
        "Polish": read_text_from_file('data/short/MalyKsiaze/Polish.txt')
    }

    """Zmienne pomocnicze"""
    print_debug = False  # Włączenie wyświetlania kodowanej i odzyskanej wiadomości
    iterations_stability = 1  # Liczba iteracji testu stabilności
    iterations_cpu = 1  # Liczba iteracji testu obciążenia CPU
    entropy_values = {} # Wartości entropii
    text_sizes = {} # Długość tekst
    segment_length = 1500  # Długość segmentu dla kodowania arytmetycznego

    """Przygotowanie Dataframe"""
    data = {
        "Language": [],
        "Input Entropy [bits/symbol]": [],
        "Input Size [bytes]": [],
        "Algorithm": [],
        "Time [s]": [],
        "Compressed Size [bytes]": [],
        "Entropy [bits/symbol]": [],
        "Average Code Length [bits/symbol]": [],
        "Ratio": [],
        "Information Gain [bytes]": [],
        "Efficiency": [],
        "Redundancy [bits/symbol]": [],
        "Stability Mean [s]": [],
        "Stability Min [s]": [],
        "Stability Max [s]": [],
        "Memory Usage [MiB]": [],
        "CPU Usage [%]": []
    }

    # Docelowy Dataframe
    df = pd.DataFrame(data)
    # Zmienna pomocnicza do zapisywania aktualnych wyników
    row = {}

    """Właściwa część programu"""
    for language, text in texts_full.items():
        language = language.split(" ")[0]

        print(f"Processing {language} text")

        # Oryginalny język tekstu
        results = {"Language": language}
        # Oryginalny rozmiar w bajtach
        original_size = len(text.encode('utf-8'))
        # Entropia oryginalnego tekstu
        entropy = calculate_entropy(text)

        results["Entropy"] = f"{entropy:.5f} bits per symbol"
        results["Original Size"] = f"{original_size:.5f} bytes"

        # Testowanie Huffman
        print(50 * "-")
        print("Huffman")
        huffman_compressed, huffman_codebook, huffman_avg_code_len = huffman_encode(text)

        # Czas wykonania
        huffman_time = test_execution_time_func(huffman_encode, text)
        # Wielkość skompresowana w bajtach
        huffman_compressed_size = len(huffman_compressed) / 8

        # Entropia kodu
        huffman_entropy = calculate_entropy(huffman_compressed)
        # Współczynnik kompresji — stosunek skompresowanego rozmiaru do oryginalnego
        huffman_ratio = compression_ratio(original_size, huffman_compressed_size)
        # Zysk informacyjny — różnica między oryginalnym rozmiarem a skompresowanym
        huffman_information_gain = original_size - huffman_compressed_size
        # Efektywność kodu — stosunek entropii do średniej długości kodu
        huffman_efficiency = huffman_entropy / huffman_avg_code_len
        # Redundancja — różnica między średnią długością kodu a entropią
        huffman_redundancy = huffman_avg_code_len - huffman_entropy

        # Stabilność — średni czas wykonania, minimalny i maksymalny
        huffman_stability = stability_test(huffman_encode, text, iterations=iterations_stability)
        # Pamięć — zużycie pamięci w MiB
        huffman_memory = test_memory_usage_func(huffman_encode, text)
        # Obciążenie CPU
        huffman_cpu_usage = measure_cpu_usage(huffman_encode, text, iterations=iterations_cpu)

        if print_debug:
            print(f"Decoded Huffman: {huffman_decode(huffman_compressed, huffman_codebook)}")

        # Zapisz wyniki Huffman
        results["Huffman Time"] = f"{huffman_time:.5f} seconds"
        results["Huffman Compressed Size"] = f"{huffman_compressed_size:.5f} bytes"

        results["Huffman Entropy"] = f"{huffman_entropy:.5f} bits per symbol"
        results["Huffman Average Code Length"] = f"{huffman_avg_code_len:.5f} bits per symbol"
        results["Huffman Ratio"] = f"{huffman_ratio:.5f}"
        results["Huffman Information Gain"] = f"{huffman_information_gain} bytes"
        results["Huffman Efficiency"] = f"{huffman_efficiency:.5f}"
        results["Huffman Redundancy"] = f"{huffman_redundancy:.5f} bits per symbol"

        results["Huffman Stability"] = f"mean={huffman_stability[0]:.5f}, min={huffman_stability[1]:.5f}, max={huffman_stability[2]:.5f} seconds"
        results["Huffman Memory Usage"] = f"{huffman_memory:.5f} MiB"
        results["Huffman CPU Usage"] = f"{huffman_cpu_usage} %"

        # Zapis danych do Dataframe
        df.loc[len(df)] = [
            language,
            entropy,
            original_size,
            "Huffman",
            huffman_time,
            huffman_compressed_size,
            huffman_entropy,
            huffman_avg_code_len,
            huffman_ratio,
            huffman_information_gain,
            huffman_efficiency,
            huffman_redundancy,
            huffman_stability[0],
            huffman_stability[1],
            huffman_stability[2],
            huffman_memory,
            huffman_cpu_usage
        ]

        print(f"{huffman_time:.5f} seconds")

        # Testowanie kodowanie arytmetyczne
        print(50 * "-")
        print("Arithmetic")
        arithmetic_encoded_segments, arithmetic_probabilities = arithmetic_encode_large(text, segment_length)

        # Czas wykonania
        arithmetic_time = test_execution_time_func(arithmetic_encode_large, text, segment_length)
        # Wielkość skompresowana w bajtach
        compressed_binary_segments = [struct.pack('d', segment) for segment in arithmetic_encoded_segments]
        arithmetic_compressed_size = sum(len(segment) for segment in compressed_binary_segments)

        # Entropia kodu
        arithmetic_entropy = calculate_entropy("".join(map(str, arithmetic_encoded_segments)))
        # Średnia długość kodu — dla kodowania arytmetycznego średnia długość kodu jest równoważna entropii
        arithmetic_avg_code_len = arithmetic_entropy
        # Współczynnik kompresji
        arithmetic_ratio = compression_ratio(original_size, arithmetic_compressed_size)
        # Zysk informacyjny
        arithmetic_information_gain = original_size - arithmetic_compressed_size
        # Efektywność kodu
        arithmetic_efficiency = arithmetic_entropy / arithmetic_avg_code_len
        # Redundancja
        arithmetic_redundancy = arithmetic_avg_code_len - arithmetic_entropy

        # Stabilność
        arithmetic_stability = stability_test(arithmetic_encode_large, text, segment_length,
                                              iterations=iterations_stability)
        # Pamięć
        arithmetic_memory = test_memory_usage_func(arithmetic_encode_large, text, segment_length)
        # Obciążenie CPU
        arithmetic_cpu_usage = measure_cpu_usage(arithmetic_encode_large, text, segment_length,
                                                 iterations=iterations_cpu)

        # Zapisanie zdekodowanego tekstu do pliku
        decoded_text = arithmetic_decode_large(arithmetic_encoded_segments, segment_length, arithmetic_probabilities)
        if language == "English":
            with open(f"results/decoded_{language}.txt", "w") as file:
                file.write(decoded_text)

        # Debugowanie
        if print_debug:
            print(f"Decoded Arithmetic: {decoded_text}")

        # Zapisz wyniki Arithmetic
        results["Arithmetic Time"] = f"{arithmetic_time:.5f} seconds"
        results["Arithmetic Compressed Size"] = f"{arithmetic_compressed_size:.5f} bytes"

        results["Arithmetic Entropy"] = f"{arithmetic_entropy:.5f} bits per symbol"
        results["Arithmetic Average Code Length"] = f"{arithmetic_avg_code_len:.5f} bits per symbol"
        results["Arithmetic Ratio"] = f"{arithmetic_ratio:.5f}"
        results["Arithmetic Information Gain"] = f"{arithmetic_information_gain} bytes"
        results["Arithmetic Efficiency"] = f"{arithmetic_efficiency:.5f}"
        results["Arithmetic Redundancy"] = f"{arithmetic_redundancy:.5f} bits per symbol"

        results["Arithmetic Stability"] = f"mean={arithmetic_stability[0]:.5f}, min={arithmetic_stability[1]:.5f}, max={arithmetic_stability[2]:.5f} seconds"
        results["Arithmetic Memory Usage"] = f"{arithmetic_memory:.5f} MiB"
        results["Arithmetic CPU Usage"] = f"{arithmetic_cpu_usage} %"
        print(f"{arithmetic_time:.5f} seconds")

        # Zapis danych do Dataframe
        df.loc[len(df)] = [
            language,
            entropy,
            original_size,
            "Arithmetic",
            arithmetic_time,
            arithmetic_compressed_size,
            arithmetic_entropy,
            arithmetic_avg_code_len,
            arithmetic_ratio,
            arithmetic_information_gain,
            arithmetic_efficiency,
            arithmetic_redundancy,
            arithmetic_stability[0],
            arithmetic_stability[1],
            arithmetic_stability[2],
            arithmetic_memory,
            arithmetic_cpu_usage
        ]

        # Testowanie ANS
        print(50 * "-")
        print("ANS")
        ans_table = build_tans_table(text)
        encoded_ans_state, encoded_ans = tans_encode(text, ans_table)

        # Czas wykonania
        ans_time = test_execution_time_func(tans_encode, text, ans_table)
        # Wielkość skompresowana w bajtach
        ans_compressed_size = len(encoded_ans)

        # Entropia kodu
        ans_entropy = calculate_entropy(str(encoded_ans))

        # Średnia długość kodu — w przypadku ANS średnia długość kodu to entropia
        ans_avg_code_len = ans_entropy
        # Współczynnik kompresji
        ans_ratio = compression_ratio(original_size, ans_compressed_size)
        # Zysk informacyjny
        ans_information_gain = original_size - ans_compressed_size
        # Efektywność kodu
        ans_efficiency = ans_entropy / ans_avg_code_len
        # Redundancja
        ans_redundancy = ans_avg_code_len - ans_entropy

        # Stabilność
        ans_stability = stability_test(lambda t: tans_encode(t, ans_table), text, iterations=100)
        # Pamięć
        ans_memory = test_memory_usage_func(tans_encode, text, ans_table)
        # Obciążenie CPU
        ans_cpu_usage = measure_cpu_usage(tans_encode, text, ans_table, iterations=iterations_cpu)

        # Debugowanie
        if print_debug:
            decoded_ans = tans_decode(encoded_ans, encoded_ans_state, ans_table)
            print(f"Decoded ANS: {decoded_ans}")

        # Zapisz wyniki ANS
        results["ANS Time"] = f"{ans_time:.5f} seconds"
        results["ANS Compressed Size"] = f"{ans_compressed_size:.5f} bytes"

        results["ANS Entropy"] = f"{ans_entropy:.5f} bits per symbol"
        results["ANS Average Code Length"] = f"{ans_avg_code_len:.5f} bits per symbol"
        results["ANS Ratio"] = f"{ans_ratio:.5f}"
        results["ANS Information Gain"] = f"{ans_information_gain} bytes"
        results["ANS Efficiency"] = f"{ans_efficiency:.5f}"
        results["ANS Redundancy"] = f"{ans_redundancy:.5f} bits per symbol"

        results["ANS Stability"] = f"mean={ans_stability[0]:.5f}, min={ans_stability[1]:.5f}, max={ans_stability[2]:.5f} seconds"
        results["ANS Memory Usage"] = f"{ans_memory:.5f} MiB"
        results["ANS CPU Usage"] = f"{ans_cpu_usage} %"

        # Zapis danych do Dataframe
        df.loc[len(df)] = [
            language,
            entropy,
            original_size,
            "ANS",
            ans_time,
            ans_compressed_size,
            ans_entropy,
            ans_avg_code_len,
            ans_ratio,
            ans_information_gain,
            ans_efficiency,
            ans_redundancy,
            ans_stability[0],
            ans_stability[1],
            ans_stability[2],
            ans_memory,
            ans_cpu_usage
        ]

        # Zapisz wyniki do pliku
        filename = f"results_{language.lower()}.txt"
        save_results_to_file(filename, results)
        print(f"Results for {language} saved to {filename}\n")
        print(23 * "=", "DONE", 23 * "=")

    # Zapisz wyniki do pliku CSV
    df.to_csv("results/results.csv", index=False)