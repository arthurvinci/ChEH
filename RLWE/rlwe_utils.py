from sage.all import *

from typing import Callable


def generate_gadget_matrix(RQ: QuotientRing, n: int) -> Matrix:
    """
    Generates the G gadget matrix of size n x 2.

    :param RQ: The quotient ring Z_q[X]/(X^N + 1).
    :param n: Number of rows of the matrix.
    :return: The G gadget matrix of size n x 2.
    """
    g = vector([2 ** i for i in range(n)])
    return matrix(RQ, n, 2, lambda i, j: g[i - n] if (j == 0 and i < n) or (j == 1 and i >= n) else 0)


def poly_bit_decomp(RQ: QuotientRing, poly, n: int) -> vector:
    """
    Generates the bit decomposition for a polynomial.

    :param RQ: The quotient ring Z_q[X]/(X^N + 1).
    :param poly: The input polynomial for bit decomposition.
    :param n:number of bits of the decomposition.
    :return: A vector representing the result of polynomial bit decomposition.
    """
    result = zero_vector(RQ, n)
    coeffs = poly.list()

    for k in range(len(coeffs)):
        for l in range(n):
            new_coeff = RQ((coeffs[k] >> l) % 2)
            result[l] += new_coeff * RQ.gen() ** k

    return result


def matrix_poly_bit_decomp(RQ: QuotientRing, matrix: Matrix, n: int) -> Matrix:
    """
    Generates the polynomial bit decomposition matrix of a given polynomial matrix.

    :param RQ: The quotient ring Z_q[X]/(X^N + 1).
    :param matrix: Polynomial matrix for which to perform the polynomial bit decomposition.
    :param n: number of bits of the decomposition
    :return: The resulting polynomial bit decomposition matrix.
    """
    new_rows = matrix.nrows()
    new_cols = n * matrix.ncols()

    result_matrix = Matrix(RQ, new_rows, new_cols)

    for i in range(matrix.nrows()):
        for j in range(matrix.ncols()):
            poly = matrix[i, j]
            bit_decomp = poly_bit_decomp(RQ, poly, n)
            for k in range(n):
                result_matrix[i, j*n + k] = bit_decomp[k]

    return result_matrix


def generate_error_poly(RQ: QuotientRing, d: int, error_distribution: Callable[[], int]):
    """
    Generates a polynomial in the quotient ring RQ with coefficients determined by the error distribution.

    :param RQ: The quotient ring Z_q[X]/(X^N + 1).
    :param d: The degree of the polynomial.
    :param error_distribution: A callable function returning an integer representing the error term.
    :return: A polynomial in the quotient ring RQ.
    """
    return RQ.sum([error_distribution() * RQ.gen() ** i for i in range(d)])


def generate_random_poly_vector(RQ: QuotientRing, n: int):
    """
    Generates a vector of random polynomials in the quotient ring RQ.

    :param RQ: The quotient ring Z_q[X]/(X^N + 1).
    :param n: The size of the vector.
    :return: A vector of random polynomials in the quotient ring RQ.
    """
    return vector([RQ.random_element() for _ in range(n)])


def generate_error_poly_matrix(RQ: QuotientRing, d: int, m: int, n: int, error_distribution: Callable[[], int]):
    """
    Generates a matrix of polynomials in the quotient ring RQ with coefficients determined by the error distribution.

    :param RQ: The quotient ring Z_q[X]/(X^N + 1).
    :param d: The degree of the polynomials.
    :param m: The number of rows in the matrix.
    :param n: The number of columns in the matrix.
    :param error_distribution: A callable function returning an integer representing the error term.
    :return: A matrix of polynomials in the quotient ring RQ.
    """
    return matrix(RQ, m, n, lambda i, j: generate_error_poly(RQ, d, error_distribution))
