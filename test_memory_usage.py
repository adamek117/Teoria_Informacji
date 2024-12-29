from memory_profiler import memory_usage

# Funkcja do testowania zużycia pamięci
def test_memory_usage_func(algorithm, text):
    mem_usage = memory_usage((algorithm, (text,)))  # Mierz zużycie pamięci podczas wykonania algorytmu
    return max(mem_usage)  # Zwróć maksymalne zużycie pamięci