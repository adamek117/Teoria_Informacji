import time

# Funkcja do testowania czasu wykonania
def test_execution_time_func(algorithm, text):
    start_time = time.time()
    algorithm(text)  # Wywołaj algorytm kompresji
    return time.time() - start_time  # Zwróć czas wykonania