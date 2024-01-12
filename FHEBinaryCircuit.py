from typing import TypeVar, Generic, List, Callable
from BinaryGate import BinaryGate
from FHEGates.ANDGate import ANDGate
from FHEGates.NANDGate import NANDGate
from FHEGates.NOTGate import NOTGate
from FHEGates.ORGate import ORGate
from FHEGates.XORGate import XORGate
from WireGate import WireGate

CypheredTextType = TypeVar('CypheredTextType')


class FHEBinaryCircuit(Generic[CypheredTextType]):

    def __init__(self, one: CypheredTextType, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        self.depths: List[List[BinaryGate[CypheredTextType]]] = []
        self.gates = dict()

        nand_gate = NANDGate[CypheredTextType](one, mul)
        self.gates["nand"] = nand_gate
        self.gates["and"] = ANDGate[CypheredTextType](mul)
        self.gates["or"] = ORGate[CypheredTextType](mul)
        self.gates["xor"] = XORGate[CypheredTextType]()
        self.gates["not"] = NOTGate[CypheredTextType](one)
        self.gates["wire"] = WireGate[CypheredTextType]()

    def add_depth(self, str_depth: List[str]) -> None:
        """
        Adds a depth to the circuit.
        :param str_depth: new gate depth
        :return:
        """

        depth = [self._get_gate(str_gate) for str_gate in str_depth]
        # Check compatibility with previous depth if needed
        if len(self.depths) > 0:
            # outputs are equal to number of gates
            previous_outputs = len(self.depths[-1])
            depth_inputs = inputs_amount(depth)
            if previous_outputs != depth_inputs:
                raise ValueError("Could not parse circuit: depths are not compatible!")

        self.depths.append(depth)

    def evaluate(self, inputs: List[CypheredTextType]):

        if len(self.depths) == 0:
            raise ValueError("Cannot evaluate an empty circuit!")

        # Check compatibility with circuit input
        circuit_input = inputs_amount(self.depths[0])
        if circuit_input != len(inputs):
            raise ValueError("The amount of inputs does not match the circuit inputs")

        result = inputs
        for depth in self.depths:
            result = evaluate_depth(depth, result)

        return result

    def _get_gate(self, name: str) -> BinaryGate[CypheredTextType]:
        raw_name = name.lower()

        ret = self.gates.get(raw_name)

        if ret is None:
            raise ValueError("Could not recognise gate {}!".format(name))
        else:
            return ret


def inputs_amount(depth: List[BinaryGate[CypheredTextType]]) -> int:
    inputs_nb = 0
    for gate in depth:
        inputs_nb += gate.inputs()
    return inputs_nb


def evaluate_depth(depth: List[BinaryGate[CypheredTextType]], inputs: List[CypheredTextType]) -> List[CypheredTextType]:
    inputs_index = 0
    result = []
    for gate in depth:
        result.append(gate.evaluate(inputs[inputs_index:inputs_index + gate.inputs()]))
        inputs_index += gate.inputs()

    return result
