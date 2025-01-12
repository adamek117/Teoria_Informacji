import psutil

def measure_cpu_usage(algorithm, text, *args, iterations=1000):
    """
    Funkcja obliczająca wykorzystanie CPU
    """
    process = psutil.Process()
    start_cpu = process.cpu_percent(interval=None)
    for _ in range(iterations):
        algorithm(text, *args)
    end_cpu = process.cpu_percent(interval=None)
    
    return (end_cpu - start_cpu) / iterations