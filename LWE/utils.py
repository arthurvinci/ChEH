import math
from typing import Callable

import numpy as np


def lwe_sample(n: int, q: int) -> int:
    return math.floor(np.random.normal(0, math.sqrt(n))) % q


def generate_random_matrix(m: int, n: int, q: int) -> np.ndarray:
    """
    Generates a random matrix of size m x n with integers modulus q.
    """
    return np.random.randint(0, q, size=(m, n), dtype=np.int32)


def generate_error_vector(m: int, error_function: Callable[[], int]) -> np.ndarray:
    """
    Generates a vector of size m using an error function.
    """
    return np.array([error_function() for _ in range(m)], dtype=np.int32).reshape(-1, 1)


def generate_error_matrix(m: int, n: int, error_function: Callable[[], int]) -> np.ndarray:
    """
    Generates a matrix of size m x n using an error function.
    """
    return np.array([[error_function() for _ in range(n)] for _ in range(m)], dtype=np.int32)


def generate_gadget_matrix(q: int, n: int) -> np.ndarray:
    """
    Generates the G gadget matrix of size m x n
    """
    log_q = math.ceil(math.log2(q))
    g = np.array([1 << i for i in range(log_q)], dtype=np.int32).reshape(-1, 1)
    return np.kron(np.eye(n, dtype=np.int32), g)


def bit_decomp(matrix: np.ndarray, q: int) -> np.ndarray:
    """
    Generates the bit decomposition matrix of a given matrix.
    :param matrix: matrix for which to make the bit decomposition.
    :param q: modulus of the matrix items
    :return:
    """
    decomp = math.ceil(math.log2(q))
    new_shape = (matrix.shape[0], decomp * matrix.shape[1])
    result = np.zeros(new_shape, dtype=np.int32)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            for k in range(decomp):
                result[i, j * decomp + k] = (matrix[i, j] >> k) & 1
    return result
