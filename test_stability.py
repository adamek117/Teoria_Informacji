import text_execution_time


def stability_test(algorithm, text, iterations):
    times = []
    for _ in range(iterations):
        times.append(text_execution_time.test_execution_time_func(algorithm, text))
    return sum(times) / len(times), min(times), max(times)