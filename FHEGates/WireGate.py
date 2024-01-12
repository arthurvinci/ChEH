from typing import TypeVar, List

from FHEBinaryGate import FHEBinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class WireGate(FHEBinaryGate[CypheredTextType]):
    def inputs(self) -> int:
        return 1

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        return inputs[0]
