from sage.all import *
from sage.structure.element import Vector

from typing import List, Tuple, Callable, Dict

from BinaryGate import BinaryGate
from FHEBinaryCircuit import FHEBinaryCircuit
from FHEScheme import FHEScheme
from RLWE.rlwe_utils import generate_error_poly, generate_random_poly_vector, generate_error_poly_matrix, \
    generate_gadget_matrix, matrix_poly_bit_decomp

PublicKeyType = Matrix
PrivateKeyType = Vector
CypheredTextType = Matrix
KeyGenType = Tuple[int, int, Callable[[], int]]


class RLWEGSW(FHEScheme[PublicKeyType, PrivateKeyType, CypheredTextType, KeyGenType]):
    q: int
    N: int
    log_q: int
    error_distribution: Callable[[], int]
    RQ: QuotientRing
    R2: QuotientRing
    G: Matrix
    gates: Dict[str, BinaryGate[CypheredTextType]]

    def keygen(self, parameters: KeyGenType) -> (PrivateKeyType, PublicKeyType):
        self.q, self.N, self.error_distribution = parameters[:3]
        self.log_q = math.ceil(math.log2(self.q))

        self.N = 2 ** self.N

        # Creates the polynomial ring Z_q[X]/(X^N + 1)
        R = PolynomialRing(IntegerModRing(self.q), 'X')
        self.RQ = QuotientRing(R, R.gen() ** self.N + 1)

        # Creates the polynomial ring Z_2[X]/(X^N +1)
        R2_temp = PolynomialRing(GF(2), 'X')
        self.R2 = QuotientRing(R2_temp, R2_temp.gen() ** self.N + 1)

        self.G = generate_gadget_matrix(self.RQ, 2 * self.log_q)

        a = self.RQ.random_element()
        s = generate_error_poly(self.RQ, self.N, self.error_distribution)
        e = generate_error_poly(self.RQ, self.N, self.error_distribution)
        b = -a * s + e

        pk = vector([b, a])
        sk = column_matrix([1, s])

        return sk, pk

    def encrypt(self, public_key: PublicKeyType, bit: bool) -> CypheredTextType:

        if public_key.nrows() != 1 or public_key.ncols() != 2:
            raise ValueError(f"Invalid dimensions for the public key: should be a row vector of 2 elements")

        t = generate_random_poly_vector(self.R2, 2 * self.log_q)
        f = generate_error_poly_matrix(self.RQ, self.N, 2 * self.log_q, 2, self.error_distribution)

        result = t * public_key + f
        if bit:
            result += self.G

        return result

    def decrypt(self, secret_key: PrivateKeyType, ct: CypheredTextType) -> bool:

        if secret_key.nrows() != 2 or secret_key.ncols() != 1:
            raise ValueError(f"Invalid dimensions for the secret key: should be a column vector of 2 elements")

        if ct.nrows() != 2 * self.log_q or ct.ncols() != 2:
            raise ValueError(
                f"Invalid dimensions for the cyphered text: should be a vector of {2 * self.log_q} x {2} elements (input "
                f"is {ct.nrows()} x {ct.ncols()})")

        raw_decrypt = ct * secret_key
        coeff = raw_decrypt[self.log_q - 1]
        return self.q // 4 <= coeff <= 3 * self.q // 4

    def evaluate(self, binary_circuit: List[List[str]], inputs: List[CypheredTextType]) -> CypheredTextType:

        circuit = FHEBinaryCircuit[CypheredTextType](self.G, lambda ct1, ct2: self._mul(ct1, ct2))

        for depth in binary_circuit:
            circuit.add_depth(depth)

        return circuit.evaluate(inputs)

    def _mul(self, CT1: CypheredTextType, CT2: CypheredTextType) -> CypheredTextType:
        if CT1.nrows() != 2 * self.log_q or CT1.ncols() != 2:
            raise ValueError(
                f"Invalid dimensions for the first cyphered text: should be a vector of {2 * self.log_q} x {2} elements (input "
                f"is {CT1.nrows()} x {CT1.ncols()})")

        if CT2.nrows() != 2 * self.log_q or CT2.ncols() != 2:
            raise ValueError(
                f"Invalid dimensions for the second cyphered text: should be a vector of {2 * self.log_q} x {2} elements (input "
                f"is {CT2.nrows()} x {CT2.ncols()})")

        return matrix_poly_bit_decomp(self.RQ, CT2, self.log_q) * CT1
