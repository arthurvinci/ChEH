import unittest

import numpy as np

from LWE.utils import bit_decomp, generate_gadget_matrix, generate_random_matrix
from tests_utils import generic_test


class TestLWEUtils(unittest.TestCase):

    def test_generate_gadget_matrix(self):
        q = 16
        n = 3
        expected_result = np.array(
            [[1, 0, 0], [2, 0, 0], [4, 0, 0], [8, 0, 0], [0, 1, 0], [0, 2, 0], [0, 4, 0], [0, 8, 0], [0, 0, 1],
             [0, 0, 2], [0, 0, 4], [0, 0, 8]], dtype=np.int32)
        generic_test(generate_gadget_matrix, (q, n), expected_result, "G Gadget Matrix")

    def test_bit_decomp_1(self):
        matrix = np.array([[1, 2],
                           [3, 4]])
        q = 8
        expected_result = np.array([[1, 0, 0, 0, 1, 0],
                                    [1, 1, 0, 0, 0, 1]])
        generic_test(bit_decomp, (matrix, q), expected_result, "2x2 matrix bit decomposition")

    def test_bit_decomp_2(self):
        matrix = np.array([[5, 7, 10],
                           [2, 4, 8]])
        q = 11
        expected_result = np.array([[1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
                                    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]])

        generic_test(bit_decomp, (matrix, q), expected_result, "2x3 matrix bit decomposition")

    def test_bit_decomp_mul_G(self):
        matrix = np.array([[23, 44, 32],
                           [2, 14, 27],
                           [3, 35, 23]])
        q = 45
        func = lambda: bit_decomp(matrix, q) @ generate_gadget_matrix(q, 3)

        generic_test(func, (), matrix, "3x3 matrix bit decomposition")

    def test_big_bit_decomp_mul_G(self):
        matrix = generate_random_matrix(100, 100, 128)
        func = lambda: (bit_decomp(matrix, 128) @ generate_gadget_matrix(128, 100)) % 128

        generic_test(func, (), matrix, "100x100 bit decomposition ")

