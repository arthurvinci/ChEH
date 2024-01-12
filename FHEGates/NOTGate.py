from typing import TypeVar, List

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class NOTGate(BinaryGate[CypheredTextType]):

    def __init__(self, one: CypheredTextType):
        self.one = one

    def inputs(self) -> int:
        return 1

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.one - inputs[0]
