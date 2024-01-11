import timeit

import numpy as np


def generic_test(func, args, expected_result, test_name):
    """
    A generic test method.
    :param func: function to test.
    :param args: arguments to test the function with.
    :param expected_result: expected test result for the given inputs.
    :param test_name: name associated to the test.
    """

    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()
    execution_time = end_time - start_time

    if isinstance(expected_result, np.ndarray):
        assert np.array_equal(result, expected_result), \
            f"Test failed: {func.__name__}({args}) returned {result}, " \
            f"expected {expected_result}."
    else:
        assert result == expected_result, \
            f"Test failed: {func.__name__}({args}) returned {result}, expected {expected_result}."

    print(f"{test_name} test passed in {execution_time:.6f} seconds.")


def multiple_generic_tests(func, args, expected_result, nb_of_tests, test_name):
    """
    A generic test method to test multiple time the same function.
    :param func: function to test.
    :param args: arguments to test the function with.
    :param expected_result: expected test result for the given inputs.
    :param nb_of_tests: number of times to repeat the test
    :param test_name: name associated to the test.
    """
    start_time = timeit.default_timer()
    nb_worked = 0
    for _ in range(nb_of_tests):
        result = func(*args)

        if isinstance(expected_result, np.ndarray):
            nb_worked += 1 if np.array_equal(result, expected_result) else 0
        else:
            nb_worked += 1 if result == expected_result else 0

    end_time = timeit.default_timer()
    execution_time = end_time - start_time

    assert nb_worked == nb_of_tests, f"Only {nb_worked}/{nb_of_tests} test worked for test {test_name}"

    print(f"All {nb_of_tests} passed for {test_name} in {execution_time:.6f} seconds.")
