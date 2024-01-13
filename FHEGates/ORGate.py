from typing import TypeVar, List, Callable

from FHEBinaryGate import FHEBinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class ORGate(FHEBinaryGate[CypheredTextType]):

    def __init__(self, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        self.mul = mul

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.mul(inputs[0], inputs[1]) + inputs[0] + inputs[1]
