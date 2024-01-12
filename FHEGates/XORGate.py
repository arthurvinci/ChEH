from typing import TypeVar, List

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class XORGate(BinaryGate[CypheredTextType]):

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return inputs[0] + inputs[1]
