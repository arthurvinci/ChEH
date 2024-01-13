from sage.all import *
from sage.structure.element import Vector

from typing import List, Tuple, Callable

from FHEBinaryCircuit import FHEBinaryCircuit
from FHEScheme import FHEScheme
from RLWE.rlwe_utils import generate_error_poly, generate_random_poly_vector, generate_error_poly_matrix, \
    generate_gadget_matrix, matrix_poly_bit_decomp

PublicKeyType = Matrix
PrivateKeyType = Vector
CypheredTextType = Matrix
KeyGenType = Tuple[int, int, Callable[[], int]]


class RLWEGSW(FHEScheme[PublicKeyType, PrivateKeyType, CypheredTextType, KeyGenType]):
    """
    RLWEGSW (Ring-LWE-based GSW) is an implementation of a Fully Homomorphic Encryption (FHE) scheme
    based on Ring-LWE.

    The RLWEGSW class extends the abstract FHEScheme class and provides concrete implementations for
    key generation, encryption, decryption, and circuit evaluation.

    Attributes:
        q: Modulus for the RLWE ring.
        N: Ring dimension (degree of the polynomial ring).
        log_q: Logarithm (base 2) of the modulus q.
        error_distribution: Callable function to generate random error terms.
        RQ: Quotient ring Z_q[X]/(X^N + 1) for RLWE.
        R2: Quotient ring Z_2[X]/(X^N + 1) for RLWE.
        G: Gadget matrix used in encryption.

    Methods:
        keygen: Generates a key pair for RLWEGSW.
        encrypt: Encrypts a boolean bit into a cyphered text.
        decrypt: Decrypts a cyphered text to obtain the original boolean bit.
        evaluate: Evaluates a binary circuit for a given set of cyphered text inputs.
        _mul: Internal method for multiplication operation in RLWEGSW.
    """

    q: int
    N: int
    log_q: int
    error_distribution: Callable[[], int]
    RQ: QuotientRing
    R2: QuotientRing
    G: Matrix

    def keygen(self, parameters: KeyGenType) -> (PrivateKeyType, PublicKeyType):

        """
        Generates a key pair.

        :param parameters: Tuple containing modulus q, n such that 2**N is the ring dimension, and error distribution
                           function.
        :return: A tuple containing the private key and the public key.
        """

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
        """
        Encrypts a boolean bit into a cyphered text.

        :param public_key: Public key used for encryption.
        :param bit: The boolean bit to be encrypted (True or False).
        :return: A cyphered text representing the encrypted bit.
        """

        t = generate_random_poly_vector(self.RQ, 2 * self.log_q)
        f = generate_error_poly_matrix(self.RQ, self.N, 2 * self.log_q, 2, self.error_distribution)

        result = t * public_key.T + f

        if bit:
            result += self.G

        return result

    def decrypt(self, secret_key: PrivateKeyType, ct: CypheredTextType) -> bool:
        """
        Decrypts a cyphered text.

        :param secret_key: Secret key used for decryption.
        :param ct: Cyphered text to be decrypted.
        :return: The decrypted boolean bit.
        """

        raw_decrypt = ct * secret_key
        poly = raw_decrypt[self.log_q - 1]
        coeff = poly.list()[0]
        return self.q // 4 <= coeff <= 3 * self.q // 4

    def evaluate(self, binary_circuit: List[List[str]], inputs: List[CypheredTextType]) -> CypheredTextType:
        """
        Evaluates a binary circuit for a given set of cyphered text inputs.

        :param binary_circuit: List of circuit depths where each depth consists of strings with gate names:
                               AND, NAND, OR, XOR, NOT, or WIRE (no gate).
        :param inputs: Cyphered texts for which to evaluate the circuit.
        :return: The cyphered text result after evaluating the circuit.
        """

        circuit = FHEBinaryCircuit[CypheredTextType](self.G, lambda ct1, ct2: self._mul(ct1, ct2))

        for depth in binary_circuit:
            circuit.add_depth(depth)

        return circuit.evaluate(inputs)

    def _mul(self, CT1: CypheredTextType, CT2: CypheredTextType) -> CypheredTextType:
        """
        Internal method for multiplication operation.

        :param CT1: First cyphered text for multiplication.
        :param CT2: Second cyphered text for multiplication.
        :return: The result of the multiplication operation.
        """

        if CT1.nrows() != 2 * self.log_q or CT1.ncols() != 2:
            raise ValueError(
                f"Invalid dimensions for the first cyphered text: should be a vector of {2 * self.log_q} x {2} elements (input "
                f"is {CT1.nrows()} x {CT1.ncols()})")

        if CT2.nrows() != 2 * self.log_q or CT2.ncols() != 2:
            raise ValueError(
                f"Invalid dimensions for the second cyphered text: should be a vector of {2 * self.log_q} x {2} elements (input "
                f"is {CT2.nrows()} x {CT2.ncols()})")

        return matrix_poly_bit_decomp(self.RQ, CT2, self.log_q) * CT1
