import text_execution_time


def stability_test(algorithm, text, iterations, *args):
    times = []
    for _ in range(iterations):
        times.append(text_execution_time.test_execution_time_func(algorithm, text, *args))
    return sum(times) / len(times), min(times), max(times)