from typing import TypeVar, List

from FHEBinaryGate import FHEBinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class XORGate(FHEBinaryGate[CypheredTextType]):

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return inputs[0] + inputs[1]
