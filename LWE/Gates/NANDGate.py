from typing import TypeVar, List, Callable

import numpy as np

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class NANDGate(BinaryGate[CypheredTextType]):

    def __init__(self, G: np.ndarray, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        self.G = G
        self.mul = mul

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.G - self.mul(inputs[0], inputs[1])
