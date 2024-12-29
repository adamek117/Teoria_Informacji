import struct
from ANS import test_tans
from Arythmetic_Code import arithmetic_encode
from Huffman_Code import huffman_encode
from Read_file import read_text_from_file
from test_compression import compression_ratio
from test_entropy import calculate_entropy
from test_measure_cpu_usage import measure_cpu_usage
from test_memory_usage import test_memory_usage_func
from test_stability import stability_test
from text_execution_time import test_execution_time_func


if __name__ == '__main__':
    texts ={
        "Polish": read_text_from_file('Polski_Puchatek.txt'),
        "English":read_text_from_file('English_Puchatek.txt'),
        "French": read_text_from_file('French_Puchatek.txt'),
        "Hungary":read_text_from_file('Hungary_Puchatek.txt')
    }

    text = read_text_from_file('Polski_Puchatek.txt')
    print("Puchatek po polsku")
    entropy = calculate_entropy(text)
    print(f"Entropy of polish text: {entropy:.5f} bits per symbol")
    original_size = len(text.encode('utf-8'))  # Rozmiar oryginalny w bajtach
    # Testowanie Huffman
    compressed_huffman, codebook =  huffman_encode(text)
    huffman_time = test_execution_time_func(huffman_encode, text)
    huffman_memory = test_memory_usage_func(huffman_encode, text)
    huffman_entropy = calculate_entropy(compressed_huffman)
    huffman_stability = stability_test(huffman_encode,text,100)
    huffman_cpu_usage = measure_cpu_usage(huffman_encode, text)
    huffman_compressed_size = len(compressed_huffman) / 8  # Rozmiar skompresowany w bajtach
    huffman_ratio = compression_ratio(original_size, huffman_compressed_size)
    # Testowanie kodowanie arytmetyczne
    encoded_arithmetic = arithmetic_encode(text)
    arithmetic_time = test_execution_time_func(arithmetic_encode,text)
    arithmetic_memory = test_memory_usage_func(arithmetic_encode,text)
    entropy_arithmetic = calculate_entropy(str(encoded_arithmetic))
    stability_entropy = stability_test(arithmetic_encode,text,100)
    arithmetic_cpu_usage = measure_cpu_usage(arithmetic_encode, text)
    compressed_binary = struct.pack('d', encoded_arithmetic)  # 'd' oznacza double (8 bajtów)
    arithmetic_compressed_size = len(compressed_binary)  # Rozmiar w bajtach
    arithmetic_ratio = compression_ratio(original_size, arithmetic_compressed_size)
    # Porównanie wyników
    print(f"Huffman compression time: {huffman_time:.5f} seconds")
    print(f"Compressed Huffman size: {len(compressed_huffman)} bits")
    print(f"Huffman compression memory usage: {huffman_memory:.5f} MiB")
    print(f"Entropy after Huffman compression: {huffman_entropy:.5f} bits per symbol")
    print(f"Huffman stability: mean={huffman_stability[0]:.5f}, min={huffman_stability[1]:.5f}, max={huffman_stability[2]:.5f} seconds")
    print(f"Huffman cpu usage: {huffman_cpu_usage}")
    print(f"Huffman ratio: {huffman_ratio}")
    print(f"Arithmetic encoding value: {encoded_arithmetic}")
    print(f"Arithmetic encoding time: {arithmetic_time:.5f} seconds")
    print(f"Arithmetic encoding memory usage: {arithmetic_memory:.5f} MiB")
    print(f"Entropy after Arithmetic compression: {entropy_arithmetic:.5f} bits per symbol")
    print(f"Entropy stability: mean={stability_entropy[0]:.5f}, min={stability_entropy[1]:.5f}, max={stability_entropy[2]:.5f} seconds")
    print(f"Arithmetic cpu usage: {arithmetic_cpu_usage}")
    print(f"Arithmetic ratio: {arithmetic_ratio}")

    test_tans(text)

#text = read_text_from_file('Hungary_Puchatek.txt')
#print("Puchatek po węgiersku")
# Testowanie Huffman
#start_time = time.time()
#compressed_huffman, codebook =  huffman_encode(text)
#huffman_time = time.time() - start_time

# Testowanie kodowanie arytmetyczne
#start_time = time.time()
#encoded_arithmetic = arithmetic_encode(text)
#arithmetic_time = time.time() - start_time

# Porównanie wyników
#print(f"Huffman compression time: {huffman_time} seconds")
#print(f"Arithmetic encoding time: {arithmetic_time} seconds")
#print(f"Compressed Huffman size: {len(compressed_huffman)} bits")
##print(f"Arithmetic encoding value: {encoded_arithmetic}")


#text = read_text_from_file('English_Puchatek.txt')
#print("Puchatek po angielsku")

# Testowanie Huffman
#start_time = time.time()
#compressed_huffman, codebook =  huffman_encode(text)
#huffman_time = time.time() - start_time

# Testowanie kodowanie arytmetyczne
#start_time = time.time()
#encoded_arithmetic = arithmetic_encode(text)
#arithmetic_time = time.time() - start_time

# Porównanie wyników
#print(f"Huffman compression time: {huffman_time} seconds")
#print(f"Arithmetic encoding time: {arithmetic_time} seconds")
#print(f"Compressed Huffman size: {len(compressed_huffman)} bits")
#print(f"Arithmetic encoding value: {encoded_arithmetic}")


#text = read_text_from_file('French_Puchatek.txt')
#print("Puchatek po francusku")

# Testowanie Huffman
#start_time = time.time()
#compressed_huffman, codebook =  huffman_encode(text)
#huffman_time = time.time() - start_time

# Testowanie kodowanie arytmetyczne
#start_time = time.time()
#encoded_arithmetic = arithmetic_encode(text)
#arithmetic_time = time.time() - start_time

# Porównanie wyników
#print(f"Huffman compression time: {huffman_time} seconds")
#print(f"Arithmetic encoding time: {arithmetic_time} seconds")
#print(f"Compressed Huffman size: {len(compressed_huffman)} bits")
#print(f"Arithmetic encoding value: {encoded_arithmetic}")