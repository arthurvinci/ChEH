from typing import TypeVar, List, Callable

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class ANDGate(BinaryGate[CypheredTextType]):

    def __init__(self, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        self.mul = mul

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.mul(inputs[0], inputs[1])
