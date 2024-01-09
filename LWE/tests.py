import numpy as np

from LWE.math_utils import bit_decomp, generate_gadget_matrix


def test_bit_decomp():
    # Test case 1
    matrix1 = np.array([[1, 2],
                        [3, 4]])
    q1 = 8
    expected_result1 = np.array([[1, 0, 0, 0, 1, 0],
                                 [1, 1, 0, 0, 0, 1]])
    result1 = bit_decomp(matrix1, q1)
    assert np.array_equal(result1, expected_result1)

    # Test case 2
    matrix2 = np.array([[5, 7, 10],
                        [2, 4, 8]])
    q2 = 11
    expected_result2 = np.array([[1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
                                 [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]])
    result2 = bit_decomp(matrix2, q2)
    assert np.array_equal(result2, expected_result2)

    # Test case 3
    matrix3 = np.array([[23, 44, 32],
                        [2, 14, 27],
                        [3, 35, 23]])
    q3 = 45
    decomp = bit_decomp(matrix3, q3)
    result = decomp @ generate_gadget_matrix(q3, 3)
    assert np.array_equal(matrix3, result)
