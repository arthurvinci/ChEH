from typing import TypeVar, List

from BinaryGate import BinaryGate
from LWE.Gates.NANDGate import NANDGate

CypheredTextType = TypeVar('CypheredTextType')


class XORGate(BinaryGate[CypheredTextType]):

    def __init__(self, NAND: NANDGate[CypheredTextType]):
        self.NAND = NAND

    def inputs(self) -> int:
        return 2

    def evaluate(self, inputs: List[CypheredTextType]) -> CypheredTextType:
        temp_1 = self.NAND.evaluate(inputs)
        temp_2 = self.NAND.evaluate([temp_1, inputs[0]])
        temp_3 = self.NAND.evaluate([temp_1, inputs[1]])

        return self.NAND.evaluate([temp_2, temp_3])
