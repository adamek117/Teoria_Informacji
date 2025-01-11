import struct
import os
from ans import test_tans, tans_encode, tans_decode, build_tans_table
from arythmetic_code import arithmetic_encode, arithmetic_decode
from huffman_code import huffman_encode, huffman_decode
from read_file import read_text_from_file
from test_compression import compression_ratio
from test_entropy import calculate_entropy
from test_measure_cpu_usage import measure_cpu_usage
from test_memory_usage import test_memory_usage_func
from test_stability import stability_test
from text_execution_time import test_execution_time_func

def ensure_results_dir():
    os.makedirs("results", exist_ok=True)

# Funkcja do zapisywania wyników do pliku
def save_results_to_file(filename, results):
    ensure_results_dir()
    with open(os.path.join("results", filename), "w") as file:
        for key, value in results.items():
            file.write(f"{key}: {value}\n")

if __name__ == '__main__':
    texts = {
        "Polish": read_text_from_file('data/Polski_Puchatek.txt'),
        "English": read_text_from_file('data/English_Puchatek.txt'),
        "French": read_text_from_file('data/French_Puchatek.txt'),
        "Hungary": read_text_from_file('data/Hungary_Puchatek.txt')
    }

    for language, text in texts.items():
        print(f"Processing {language} text")

        results = {"Language": language}
        entropy = calculate_entropy(text)
        results["Entropy"] = f"{entropy:.5f} bits per symbol"

        original_size = len(text.encode('utf-8'))  # Rozmiar oryginalny w bajtach

        # Testowanie Huffman
        compressed_huffman, codebook = huffman_encode(text)
        huffman_time = test_execution_time_func(huffman_encode, text)
        huffman_memory = test_memory_usage_func(huffman_encode, text)
        huffman_entropy = calculate_entropy(compressed_huffman)
        huffman_stability = stability_test(huffman_encode, text, 100)
        huffman_cpu_usage = measure_cpu_usage(huffman_encode, text)
        huffman_compressed_size = len(compressed_huffman) / 8  # Rozmiar skompresowany w bajtach
        huffman_ratio = compression_ratio(original_size, huffman_compressed_size)
        print(f"Decoded Huffman: {huffman_decode(compressed_huffman, codebook)}")

        # Zapisz wyniki Huffman
        results["Huffman Time"] = f"{huffman_time:.5f} seconds"
        results["Huffman Memory Usage"] = f"{huffman_memory:.5f} MiB"
        results["Huffman Entropy"] = f"{huffman_entropy:.5f} bits per symbol"
        results["Huffman Stability"] = f"mean={huffman_stability[0]:.5f}, min={huffman_stability[1]:.5f}, max={huffman_stability[2]:.5f} seconds"
        results["Huffman CPU Usage"] = huffman_cpu_usage
        results["Huffman Ratio"] = huffman_ratio

        # Testowanie kodowanie arytmetyczne
        encoded_arithmetic, arithmetic_prob = arithmetic_encode(text)
        print(f"Encoded arithmetic: {encoded_arithmetic}")
        arithmetic_time = test_execution_time_func(arithmetic_encode, text)
        arithmetic_memory = test_memory_usage_func(arithmetic_encode, text)
        entropy_arithmetic = calculate_entropy(str(encoded_arithmetic))
        stability_entropy = stability_test(arithmetic_encode, text, 100)
        arithmetic_cpu_usage = measure_cpu_usage(arithmetic_encode, text)
        compressed_binary = struct.pack('d', encoded_arithmetic)  # 'd' oznacza double (8 bajtów)
        arithmetic_compressed_size = len(compressed_binary)  # Rozmiar w bajtach
        arithmetic_ratio = compression_ratio(original_size, arithmetic_compressed_size)
        print(f"Decoded arithmetic: {arithmetic_decode(encoded_arithmetic, len(text), arithmetic_prob )}")

        # Zapisz wyniki kodowanie arytmetyczne
        results["Arithmetic Time"] = f"{arithmetic_time:.5f} seconds"
        results["Arithmetic Memory Usage"] = f"{arithmetic_memory:.5f} MiB"
        results["Arithmetic Entropy"] = f"{entropy_arithmetic:.5f} bits per symbol"
        results["Arithmetic Stability"] = f"mean={stability_entropy[0]:.5f}, min={stability_entropy[1]:.5f}, max={stability_entropy[2]:.5f} seconds"
        results["Arithmetic CPU Usage"] = arithmetic_cpu_usage
        results["Arithmetic Ratio"] = arithmetic_ratio

        # Testowanie ANS
        ans_table = build_tans_table(text)
        encoded_ans_state, encoded_ans = tans_encode(text, ans_table)
        ans_time = test_execution_time_func(tans_encode, text, ans_table)
        ans_memory = test_memory_usage_func(tans_encode, text, ans_table)
        entropy_ans = calculate_entropy(str(encoded_ans))
        ans_stability = stability_test(lambda t: tans_encode(t, ans_table), text, 100)
        ans_cpu_usage = measure_cpu_usage(tans_encode, text, ans_table)
        ans_compressed_size = len(encoded_ans)  # Rozmiar w bajtach (dlugosc listy)
        ans_ratio = compression_ratio(original_size, ans_compressed_size)
        print(f"Decoded ANS: {tans_decode(encoded_ans, encoded_ans_state, ans_table)}")

        # Zapisz wyniki ANS
        results["ANS Time"] = f"{ans_time:.5f} seconds"
        results["ANS Memory Usage"] = f"{ans_memory:.5f} MiB"
        results["ANS Entropy"] = f"{entropy_ans:.5f} bits per symbol"
        results["ANS Stability"] = f"mean={ans_stability[0]:.5f}, min={ans_stability[1]:.5f}, max={ans_stability[2]:.5f} seconds"
        results["ANS CPU Usage"] = ans_cpu_usage
        results["ANS Ratio"] = ans_ratio


        # Zapisz wyniki do pliku
        filename = f"results_{language.lower()}.txt"
        save_results_to_file(filename, results)
        print(f"Results for {language} saved to {filename}\n")
