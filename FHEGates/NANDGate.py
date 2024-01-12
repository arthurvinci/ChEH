from typing import TypeVar, List, Callable

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class NANDGate(BinaryGate[CypheredTextType]):

    def __init__(self, one: CypheredTextType, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        self.one = one
        self.mul = mul

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.one - self.mul(inputs[0], inputs[1])
