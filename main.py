import os
import struct
import time

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


def ensure_results_dir():
    os.makedirs("results", exist_ok=True)

# Funkcja do zapisywania wyników do pliku
def save_results_to_file(filename, results):
    ensure_results_dir()
    with open(os.path.join("results", filename), "a") as file:  # Append mode
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
        # "English - Full Text": read_text_from_file('data/full/MalyKsiaze/English.txt'),
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
    save_to_txt = False  # Zapis wyników do pliku TXT
    num_runs = 100  # Liczba iteracji testu
    iterations_stability = 1  # Liczba iteracji testu stabilności
    iterations_cpu = 1  # Liczba iteracji testu obciążenia CPU
    entropy_values = {} # Wartości entropii
    text_sizes = {} # Długość tekstu
    segment_length = 1500  # Długość segmentu dla kodowania arytmetycznego

    """Przygotowanie Dataframe"""
    data = {
        "Language": [],
        "Algorithm": [],
        "Input Entropy [bits/symbol]": [],
        "Input Size [bytes]": [],
        "Encode time [s]": [],
        "Decode time [s]": [],
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
    
    # OPCJONALNE: Odczytywanie danych z pliku CSV
    if os.path.exists("results/results_multi.csv"):
        df_existing = pd.read_csv("results/results_multi.csv")
        df = pd.concat([df_existing, df], ignore_index=True)

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

        # # Run the tests multiple times
        for run in range(num_runs):
            print(f"Run {run + 1}/{num_runs}")

            # Testowanie kodowanie Huffmana
            start_time = time.time()
            huffman_compressed, huffman_codebook, huffman_avg_code_len = huffman_encode(text)

            # Czas wykonania
            huffman_time = time.time() - start_time

            # Wielkość skompresowana w bajtach
            huffman_compressed_size = len(huffman_compressed) / 8

            # Entropia kodu
            huffman_entropy = calculate_entropy(huffman_compressed)
            # Współczynnik kompresji
            huffman_ratio = compression_ratio(original_size, huffman_compressed_size)
            # Zysk informacyjny
            huffman_information_gain = original_size - huffman_compressed_size
            # Efektywność kodu
            huffman_efficiency = huffman_entropy / huffman_avg_code_len
            # Redundancja
            huffman_redundancy = huffman_avg_code_len - huffman_entropy

            # Stabilność
            huffman_stability = stability_test(huffman_encode, text, iterations=iterations_stability)
            # Pamięć
            huffman_memory = test_memory_usage_func(huffman_encode, text)
            # Obciążenie CPU
            huffman_cpu_usage = measure_cpu_usage(huffman_encode, text, iterations=iterations_cpu)

            # Czas dekodowania
            start_time = time.time()
            huffman_decode(huffman_compressed, huffman_codebook)
            huffman_decode_time = time.time() - start_time

            if print_debug:
                print(f"Decoded Huffman: {huffman_decode(huffman_compressed, huffman_codebook)}")

            print(f"{huffman_time:.5f} seconds")

            # Zapis danych do Dataframe
            df.loc[len(df)] = [
                language,
                "Huffman",
                entropy,
                original_size,
                huffman_time,
                huffman_decode_time,
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

            if run % 5 == 0:
                # Zapisz wyniki do pliku CSV
                df.to_csv("results/results_multi.csv", index=False)

            # Zapisz wyniki Huffman
            if save_to_txt:
                results["Huffman Time"] = f"{huffman_time:.5f} seconds"
                results["Huffman Compressed Size"] = f"{huffman_compressed_size:.5f} bytes"

                results["Huffman Entropy"] = f"{huffman_entropy:.5f} bits per symbol"
                results["Huffman Average Code Length"] = f"{huffman_avg_code_len:.5f} bits per symbol"
                results["Huffman Ratio"] = f"{huffman_ratio:.5f}"
                results["Huffman Information Gain"] = f"{huffman_information_gain} bytes"
                results["Huffman Efficiency"] = f"{huffman_efficiency:.5f}"
                results["Huffman Redundancy"] = f"{huffman_redundancy:.5f} bits per symbol"

                results[
                    "Huffman Stability"] = f"mean={huffman_stability[0]:.5f}, min={huffman_stability[1]:.5f}, max={huffman_stability[2]:.5f} seconds"
                results["Huffman Memory Usage"] = f"{huffman_memory:.5f} MiB"
                results["Huffman CPU Usage"] = f"{huffman_cpu_usage} %"

                # Save results to file for each run
                save_results_to_file(f"results_{language.lower()}.txt", results)

        # Zapisz wyniki do pliku CSV
        df.to_csv("results/results_multi.csv", index=False)

        # Testowanie kodowanie arytmetyczne
        print(50 * "-")
        print("Arithmetic")

        # Run the tests multiple times
        for run in range(num_runs):
            print(f"Run {run + 1}/{num_runs}")

            # Testowanie kodowanie arytmetycznego
            start_time = time.time()
            arithmetic_encoded_segments, arithmetic_probabilities = arithmetic_encode_large(text, segment_length)

            # Czas wykonania
            arithmetic_time = time.time() - start_time
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

            # Czas dekodowania
            start_time = time.time()
            arithmetic_decode_large(arithmetic_encoded_segments, segment_length, arithmetic_probabilities)
            arithmetic_decode_time = time.time() - start_time

            print(f"{arithmetic_time:.5f} seconds")

            # Zapis danych do Dataframe
            df.loc[len(df)] = [
                language,
                "Arithmetic",
                entropy,
                original_size,
                arithmetic_time,
                arithmetic_decode_time,
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

            if run % 5 == 0:
                # Zapisz wyniki do pliku CSV
                df.to_csv("results/results_multi.csv", index=False)

            if save_to_txt:
                # Zapisanie zdekodowanego tekstu do pliku
                decoded_text = arithmetic_decode_large(arithmetic_encoded_segments, segment_length,
                                                       arithmetic_probabilities)
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

                results[
                    "Arithmetic Stability"] = f"mean={arithmetic_stability[0]:.5f}, min={arithmetic_stability[1]:.5f}, max={arithmetic_stability[2]:.5f} seconds"
                results["Arithmetic Memory Usage"] = f"{arithmetic_memory:.5f} MiB"
                results["Arithmetic CPU Usage"] = f"{arithmetic_cpu_usage} %"

                # Save results to file for each run
                save_results_to_file(f"results_{language.lower()}.txt", results)

        # Zapisz wyniki do pliku CSV
        df.to_csv("results/results_multi.csv", index=False)

        # Testowanie ANS
        print(50 * "-")
        print("ANS")

        # Run the tests multiple times
        for run in range(num_runs):
            print(f"Run {run + 1}/{num_runs}")

            start_time = time.time()
            ans_table = build_tans_table(text)
            encoded_ans_state, encoded_ans = tans_encode(text, ans_table)

            # Czas wykonania
            ans_time = time.time() - start_time
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

            # Czas dekodowania
            start_time = time.time()
            decoded_ans = tans_decode(encoded_ans, encoded_ans_state, ans_table)
            ans_decode_time = time.time() - start_time

            print(f"{ans_time:.5f} seconds")

            # Zapis danych do Dataframe
            df.loc[len(df)] = [
                language,
                "ANS",
                entropy,
                original_size,
                ans_time,
                ans_decode_time,
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

            if run % 5 == 0:
                # Zapisz wyniki do pliku CSV
                df.to_csv("results/results_multi.csv", index=False)

            if save_to_txt:
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

                results[
                    "ANS Stability"] = f"mean={ans_stability[0]:.5f}, min={ans_stability[1]:.5f}, max={ans_stability[2]:.5f} seconds"
                results["ANS Memory Usage"] = f"{ans_memory:.5f} MiB"
                results["ANS CPU Usage"] = f"{ans_cpu_usage} %"
            
                # Save results to file for each run
                save_results_to_file(f"results_{language.lower()}.txt", results)

        # Zapisz wyniki do pliku CSV
        df.to_csv("results/results_multi.csv", index=False)
