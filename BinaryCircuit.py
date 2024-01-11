from typing import TypeVar, Generic, List
from BinaryGate import BinaryGate

CypheredTextType = TypeVar('CypheredTextType')


class BinaryCircuit(Generic[CypheredTextType]):

    def __init__(self):
        self.depths: List[List[BinaryGate[CypheredTextType]]] = []

    def add_depth(self, depth: List[BinaryGate[CypheredTextType]]) -> None:
        """
        Adds a depth to the circuit.
        :param depth: new gate depth
        :return:
        """

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
