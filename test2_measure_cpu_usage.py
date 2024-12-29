import psutil

def measure_cpu_usage(algorithm, text):
    """
    Mierzy czas użytkownika (user time) i systemowy (system time) CPU podczas działania algorytmu.
    """
    process = psutil.Process()
    start_times = process.cpu_times()  # Początkowe czasy użytkownika i systemu
    
    algorithm(text)  # Wykonanie algorytmu
    
    end_times = process.cpu_times()  # Końcowe czasy użytkownika i systemu
    user_time = end_times.user - start_times.user
    system_time = end_times.system - start_times.system
    
    return user_time, system_time