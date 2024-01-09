from typing import TypeVar, List

import numpy as np

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class NOTGate(BinaryGate[CypheredTextType]):

    def __init__(self, G: np.ndarray):
        self.G = G

    def inputs(self) -> int:
        return 1

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.G - inputs[0]
