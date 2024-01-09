from typing import TypeVar, List

from BinaryGate import BinaryGate
from LWE.NANDGate import NANDGate

CypheredTextType = TypeVar('CypheredTextType')


class ANDGate(BinaryGate[CypheredTextType]):

    def __init__(self, NAND: NANDGate[CypheredTextType]):
        self.NAND = NAND

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        temp = self.NAND.evaluate(inputs)
        return self.NAND.evaluate([temp, temp])
