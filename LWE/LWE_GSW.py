import math
from typing import Tuple, Callable, List, Dict

import numpy as np

from FHEBinaryCircuit import FHEBinaryCircuit
from BinaryGate import BinaryGate
from FHEScheme import FHEScheme

from LWE.lwe_utils import generate_error_matrix, generate_error_vector, generate_random_matrix, generate_gadget_matrix, \
    bit_decomp

PublicKeyType = np.ndarray
PrivateKeyType = np.ndarray
CypheredTextType = np.ndarray
KeyGenType = Tuple[int, int, Callable[[], int]]


class LWEGSW(FHEScheme[PublicKeyType, PrivateKeyType, CypheredTextType, KeyGenType]):
    q: int
    n: int
    m: int
    error_function: Callable[[], int]
    G: np.ndarray
    gates: Dict[str, BinaryGate[CypheredTextType]]

    def keygen(self, parameters: KeyGenType) -> (PrivateKeyType, PublicKeyType):
        """
        Generates a key pair for the LWE-GSW scheme.

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

        circuit = FHEBinaryCircuit[CypheredTextType](self.G, lambda ct1, ct2: self._mul(ct1, ct2))

        for depth in binary_circuit:
            circuit.add_depth(depth)

        return circuit.evaluate(inputs)

    def _mul(self, CT1: CypheredTextType, CT2: CypheredTextType) -> CypheredTextType:

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
