from typing import TypeVar, List

from BinaryGate import BinaryGate
from LWE.NANDGate import NANDGate

CypheredTextType = TypeVar('CypheredTextType')


class ORGate(BinaryGate[CypheredTextType]):

    def __init__(self, NAND: NANDGate[CypheredTextType]):
        self.NAND = NAND

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        temp_1 = self.NAND.evaluate([inputs[0], inputs[0]])
        temp_2 = self.NAND.evaluate([inputs[1], inputs[1]])
        return self.NAND.evaluate([temp_1, temp_2])
