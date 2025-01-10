import time

# Funkcja do testowania czasu wykonania
def test_execution_time_func(algorithm, text, *args):
    start_time = time.time()
    algorithm(text, *args)  # Wywołaj algorytm kompresji z dodatkowymi argumentami
    return time.time() - start_time  # Zwróć czas wykonania