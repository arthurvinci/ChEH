from typing import TypeVar, List, Callable

from FHEBinaryGate import FHEBinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class NANDGate(FHEBinaryGate[CypheredTextType]):

    def __init__(self, one: CypheredTextType, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        self.one = one
        self.mul = mul

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.one - self.mul(inputs[0], inputs[1])
