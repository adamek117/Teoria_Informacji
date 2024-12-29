import psutil

def measure_cpu_usage(algorithm, text,  iterations=1000):

    #Tutaj można po prostu wykonać bez iteracji, żeby ocenić pojedyncze działanie algorytmu
    process = psutil.Process()
    start_cpu = process.cpu_percent(interval=None)
    for _ in range(iterations):
        algorithm(text)
    end_cpu = process.cpu_percent(interval=None)
    
    return (end_cpu - start_cpu) / iterations