import zstandard as zstd

from read_file import read_text_from_file

# Przykładowe dane
def compress_data(file):
    text = read_text_from_file(file)

    # Konwersja tekstu na bajty
    data = text.encode('utf-8')

    # Kompresja
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(data)
    return compressed_data
    print("Skompresowane dane:", compressed_data)

def decompress_data(compressed_data):
    # Dekompresja
    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)
    return decompressed_data
    print("Odkodowane dane:", decompressed_data.decode('utf-8'))