from heapq import heappush, heappop, heapify
from collections import defaultdict

def build_huffman_tree(frequencies):
    heap = [[weight, [char, ""]] for char, weight in frequencies.items()]
    heapify(heap)
    
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_encode(data):
    frequencies = defaultdict(int)
    for char in data:
        frequencies[char] += 1
    huffman_tree = build_huffman_tree(frequencies)
    huffman_dict = {char: code for char, code in huffman_tree}
    encoded_data = ''.join(huffman_dict[char] for char in data)
    return encoded_data, huffman_dict

def huffman_decode(encoded_data, huffman_dict):
    reverse_dict = {code: char for char, code in huffman_dict.items()}
    current_code = ""
    decoded_output = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_dict:
            decoded_output += reverse_dict[current_code]
            current_code = ""
    return decoded_output