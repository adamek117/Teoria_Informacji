import zstandard as zstd

from read_file import read_text_from_file

# Przykładowe dane
text = read_text_from_file('data/short/Polish.txt')

# Konwersja tekstu na bajty
data = text.encode('utf-8')

# Kompresja
cctx = zstd.ZstdCompressor()
compressed_data = cctx.compress(data)
print("Skompresowane dane:", compressed_data)

# Dekompresja
dctx = zstd.ZstdDecompressor()
decompressed_data = dctx.decompress(compressed_data)
print("Odkodowane dane:", decompressed_data.decode('utf-8'))