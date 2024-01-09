from typing import TypeVar, List

from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class WireGate(BinaryGate[CypheredTextType]):
    def inputs(self) -> int:
        return 1

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return inputs[0]
