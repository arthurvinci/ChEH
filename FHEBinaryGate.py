from typing import TypeVar, Generic, List
from abc import abstractmethod

CypheredTextType = TypeVar('CypheredTextType')


class FHEBinaryGate(Generic[CypheredTextType]):
    """
    Abstract class representing a binary gate in a Fully Homomorphic Encryption binary circuit.

    Methods:
        inputs: Returns the number of inputs of this gate.
        evaluate: Evaluates the gate for the given inputs.
    """

    @abstractmethod
    def inputs(self) -> int:
        """
        Returns the number of inputs of this gate.
        """
        pass

    @abstractmethod
    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        """
        Evaluates the gate for the given inputs.
        Warning: Always assumes that the correct amount of inputs has been given.

        :param inputs: inputs for the gate
        :return: Cyphered evaluation of the gate
        """
        pass
