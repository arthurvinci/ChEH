from typing import TypeVar, Generic, List
from abc import abstractmethod, ABC

PublicKeyType = TypeVar('PublicKeyType')
PrivateKeyType = TypeVar('PrivateKeyType')
CypheredTextType = TypeVar('CypheredTextType')
KeyGenType = TypeVar('KeyGenType')


class FHEScheme(ABC, Generic[PublicKeyType, PrivateKeyType, CypheredTextType, KeyGenType]):
    """
    Abstract base class representing a Fully Homomorphic Encryption (FHE) scheme.

    This class defines the common interface for FHE schemes, including methods for key generation,
    encryption, decryption, and circuit evaluation.

    Methods:
        keygen: Generates a key pair for the FHE scheme.
        encrypt: Encrypts a boolean bit into a cyphered text.
        decrypt: Decrypts a cyphered text to obtain the original boolean bit.
        evaluate: Evaluates a binary circuit for a given set of cyphered text inputs.
    """
    @abstractmethod
    def keygen(self, parameters: KeyGenType) -> (PrivateKeyType, PublicKeyType):
        """
        Generates a key pair for a FHE scheme
        :param parameters: parameters to generate the key pair
        :return: a public and a private key
        """
        pass

    @abstractmethod
    def encrypt(self, public_key: PublicKeyType, bit: bool) -> CypheredTextType:
        """
        Encrypts the given bit into a cyphered text
        :param public_key: public key used to encrypt the bit
        :param bit: actual bit represented as a boolean
        :return: a cyphered text representing the bit
        """
        pass

    @abstractmethod
    def decrypt(self, secret_key: PrivateKeyType, ct: CypheredTextType) -> bool:
        """
        Decrypts the given cyphered text
        :param secret_key: secret key to use to decrypt the cyphered text
        :param ct: cyphered text to decrypt
        :return: the bit
        """
        pass

    @abstractmethod
    def evaluate(self, binary_circuit: List[List[str]], inputs: List[CypheredTextType]) -> CypheredTextType:
        """
        Evaluates a binary circuit for a given input
        :param binary_circuit: list of circuit depths where each depths consist of string with gate names: AND, NAND,
        OR, XOR, NOT or WIRE(no gate)
        :param inputs: cyphered texts for which to evaluate the circuit
        :return:
        """
        pass
