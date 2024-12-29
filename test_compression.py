def compression_ratio(original_size, compressed_size):
    """
    Oblicza współczynnik kompresji.
    :param original_size: Rozmiar oryginalnych danych (w bajtach).
    :param compressed_size: Rozmiar skompresowanych danych (w bajtach).
    :return: Stosunek skompresowanego rozmiaru do oryginalnego.
    """
    if original_size == 0:
        raise ValueError("Original size cannot be zero.")
    return compressed_size / original_size