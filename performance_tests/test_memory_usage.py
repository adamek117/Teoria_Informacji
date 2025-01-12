from memory_profiler import memory_usage

def test_memory_usage_func(algorithm, text, *args):
    """
    Funkcja do pomiaru zużycia pamięci
    """
    mem_usage = memory_usage((algorithm, (text, *args)))  # Mierz zużycie pamięci podczas wykonania algorytmu
    return max(mem_usage)  # Zwróć maksymalne zużycie pamięci