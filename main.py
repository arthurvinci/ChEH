from sage.all import *

from RLWE.rlwe_utils import generate_gadget_matrix

"""
if __name__ == '__main__':
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLWEUtils)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLWE))

    unittest.TextTestRunner().run(suite)
    """



q = 8
N = 4
R = PolynomialRing(IntegerModRing(q), 'X')
RQ = QuotientRing(R, R.gen() ** N + 1)

"""
# Create a 1x1 polynomial matrix with the polynomial 7X^3 + 5X^2 + 3
matrix = Matrix(RQ, [[7 * RQ.gen()**3 + 5 * RQ.gen()**2 + 3]])


# Display the original matrix
print("Original Polynomial Matrix:")
print(matrix)

# Apply polynomial bit decomposition
decomposed_matrix = poly_bit_decomp(RQ, matrix, N)

# Display the decomposed matrix
print("\nPolynomial Bit Decomposition Matrix:")
print(decomposed_matrix)
"""


