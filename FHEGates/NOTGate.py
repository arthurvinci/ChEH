from typing import TypeVar, List

from FHEBinaryGate import FHEBinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class NOTGate(FHEBinaryGate[CypheredTextType]):

    def __init__(self, one: CypheredTextType):
        self.one = one

    def inputs(self) -> int:
        return 1

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return self.one - inputs[0]
