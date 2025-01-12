from performance_tests.text_execution_time import test_execution_time_func


def stability_test(algorithm, text, iterations=1, *args):
    times = []
    for _ in range(iterations):
        times.append(test_execution_time_func(algorithm, text, *args))
    return sum(times) / len(times), min(times), max(times)