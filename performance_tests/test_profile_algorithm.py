import cProfile

def profile_algorithm(algorithm, text):
    """
    Profiluje wykorzystanie CPU przez algorytm.
    """
    profiler = cProfile.Profile()
    profiler.enable()
    algorithm(text)
    profiler.disable()
    profiler.print_stats(sort='cumulative')  # Wyświetla wyniki posortowane według zużycia CPU

