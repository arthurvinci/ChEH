import math
from typing import Tuple, Callable, List, Dict

import numpy as np

from FHEBinaryCircuit import FHEBinaryCircuit
from FHEBinaryGate import FHEBinaryGate
from FHEScheme import FHEScheme

from LWE.lwe_utils import generate_error_matrix, generate_error_vector, generate_random_matrix, generate_gadget_matrix, \
    bit_decomp

PublicKeyType = np.ndarray
PrivateKeyType = np.ndarray
CypheredTextType = np.ndarray
KeyGenType = Tuple[int, int, Callable[[], int]]


class LWEGSW(FHEScheme[PublicKeyType, PrivateKeyType, CypheredTextType, KeyGenType]):
    """
     LWEGSW (LWE based GSW) is an implementation of a Fully Homomorphic Encryption (FHE) scheme
     based on LWE.

     The LWEGSW class extends the abstract FHEScheme class and provides concrete implementations for
     key generation, encryption, decryption, and circuit evaluation.

     Attributes:
         q: Modulus for the LWE ring.
         n: Number of columns of the matrices.
         m: n times the logarithm (base 2) of the modulus q.
         error_function: Callable function to generate random error terms.
         G: Gadget matrix used in encryption.

     Methods:
         keygen: Generates a key pair for the LWEGSW scheme.
         encrypt: Encrypts a boolean bit into a cyphered text.
         decrypt: Decrypts a cyphered text to obtain the original boolean bit.
         evaluate: Evaluates a binary circuit for a given set of cyphered text inputs.
         _mul: Internal method for multiplication operation in LWEGSW.
     """
    q: int
    n: int
    m: int
    error_function: Callable[[], int]
    G: np.ndarray

    def keygen(self, parameters: KeyGenType) -> (PrivateKeyType, PublicKeyType):
        """
        Generates a key pair.

        :param parameters: A tuple containing q, n and an error function.
        :return: A tuple containing the public key and the private key.
        """

        self.q, self.n, self.error_function = parameters[:3]
        self.m = self.n * math.ceil(math.log2(self.q))
        self.G = generate_gadget_matrix(self.q, self.n)

        A = generate_random_matrix(self.m, self.n - 1, self.q)
        e = generate_error_vector(self.m, self.error_function)
        s = generate_error_vector(self.n - 1, self.error_function)
        b = (- A @ s) + e  # @ is the matrix multiplication operator in Python

        # Concatenates b
        public_key = np.concatenate((b, A), axis=1)

        # Add a 1 on top of the private key
        private_key = np.vstack((1, s))

        return public_key, private_key

    def encrypt(self, public_key: PublicKeyType, bit: bool) -> CypheredTextType:
        """
        Encrypts a boolean bit into a cyphered text.

        :param public_key: Public key used for encryption.
        :param bit: The boolean bit to be encrypted (True or False).
        :return: A cyphered text representing the encrypted bit.
        """

        # Dimension check for the public_key
        if public_key.shape != (self.m, self.n):
            raise ValueError(
                f"Invalid dimensions for the public key: should be a matrix of {self.m} x {self.n} elements")

        T = generate_error_matrix(self.m, self.m, self.error_function)
        F = generate_error_matrix(self.m, self.n, self.error_function)

        CT = T @ public_key + F

        if bit:
            CT += self.G

        return CT % self.q

    def decrypt(self, secret_key: PrivateKeyType, CT: CypheredTextType) -> bool:
        """
        Decrypts a cyphered text.

        :param secret_key: Secret key used for decryption.
        :param CT: Cyphered text to be decrypted.
        :return: The decrypted boolean bit.
        """

        # Dimension check for the secret key
        if secret_key.shape != (self.n, 1):
            raise ValueError(f"Invalid dimensions for the secret key: should be a vector of {self.m} elements")

        # Dimension check for the cyphered text
        if CT.shape != (self.m, self.n):
            raise ValueError(
                f"Invalid dimensions for the cyphered text: should be a vector of {self.m} x {self.n} elements (input "
                f"is {CT.shape[0]} x {CT.shape[1]})")

        raw_decrypt = (CT @ secret_key) % self.q

        # print(raw_decrypt)

        log_q = self.m // self.n

        return (raw_decrypt[log_q - 1] > self.q / 4) and (raw_decrypt[log_q - 1] < 3 * self.q / 4)

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

        if CT1.shape != (self.m, self.n):
            raise ValueError(
                f"Invalid dimensions for the cyphered text: should be a vector of {self.m} x {self.n} elements (input "
                f"is {CT1.shape[0]} x {CT1.shape[1]})")

        if CT2.shape != (self.m, self.n):
            raise ValueError(
                f"Invalid dimensions for the cyphered text: should be a vector of {self.m} x {self.n} elements (input "
                f"is {CT2.shape[0]} x {CT2.shape[1]})")

        CT1_bit = bit_decomp(CT1, self.q)
        return (CT1_bit @ CT2) % self.q
