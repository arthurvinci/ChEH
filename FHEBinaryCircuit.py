from typing import TypeVar, Generic, List, Callable
from FHEBinaryGate import FHEBinaryGate
from FHEGates.ANDGate import ANDGate
from FHEGates.NANDGate import NANDGate
from FHEGates.NOTGate import NOTGate
from FHEGates.ORGate import ORGate
from FHEGates.XORGate import XORGate
from FHEGates.WireGate import WireGate

CypheredTextType = TypeVar('CypheredTextType')


class FHEBinaryCircuit(Generic[CypheredTextType]):
    """
    Represents a Fully Homomorphic Encryption (FHE) binary circuit.

    This class allows the construction and evaluation of a binary circuit using FHE gates.
    The gates supported include AND, OR, XOR, NOT, and a special Wire gate.

    Attributes:
        depths: A list containing the gates organized by depth.
        gates: A dictionary containing instances of supported FHE gates.

    Methods:
        __init__: Initializes the FHEBinaryCircuit with a given FHE one value and multiplication function.
        add_depth: Adds a depth to the circuit with specified gates.
        evaluate: Evaluates the circuit for the given inputs.

    Note:
        Gates are added to the circuit by providing their names in a depth configuration.
        The supported gate names are 'nand', 'and', 'or', 'xor', 'not', and 'wire'.
    """

    def __init__(self, one: CypheredTextType, mul: Callable[[CypheredTextType, CypheredTextType], CypheredTextType]):
        """
        Initializes a new instance of FHEBinaryCircuit.

        :param one: FHE representation of the constant '1'.
        :param mul: Multiplication function for FHE operations.
        """
        self.depths: List[List[FHEBinaryGate[CypheredTextType]]] = []
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

        :param str_depth: A list of gate names for the new depth.
        :return: None
        """
        depth = [self._get_gate(str_gate) for str_gate in str_depth]
        # Check compatibility with previous depth if needed
        if len(self.depths) > 0:
            # outputs are equal to the number of gates
            previous_outputs = len(self.depths[-1])
            depth_inputs = inputs_amount(depth)
            if previous_outputs != depth_inputs:
                raise ValueError("Could not parse circuit: depths are not compatible!")

        self.depths.append(depth)

    def evaluate(self, inputs: List[CypheredTextType]):
        """
        Evaluates the circuit for the given inputs.

        :param inputs: A list of FHE-encoded inputs for the circuit.
        :return: A list of FHE-encoded outputs after circuit evaluation.
        """
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

    def _get_gate(self, name: str) -> FHEBinaryGate[CypheredTextType]:
        """
        Gets the FHE gate instance corresponding to the given gate name.

        :param name: The name of the gate.
        :return: An instance of the corresponding FHE gate.
        """
        raw_name = name.lower()

        ret = self.gates.get(raw_name)

        if ret is None:
            raise ValueError("Could not recognize gate {}!".format(name))
        else:
            return ret


def inputs_amount(depth: List[FHEBinaryGate[CypheredTextType]]) -> int:
    """
    Calculates the total number of inputs for a given depth.

    :param depth: A list of FHE gates representing a depth in the circuit.
    :return: The total number of inputs for the depth.
    """
    inputs_nb = 0
    for gate in depth:
        inputs_nb += gate.inputs()
    return inputs_nb


def evaluate_depth(depth: List[FHEBinaryGate[CypheredTextType]], inputs: List[CypheredTextType]) -> List[CypheredTextType]:
    """
    Evaluates a depth in the FHE binary circuit.

    :param depth: A list of FHE gates representing a depth in the circuit.
    :param inputs: A list of FHE-encoded inputs for the circuit.
    :return: A list of FHE-encoded outputs after evaluating the given depth.
    """
    inputs_index = 0
    result = []

    for gate in depth:
        result.append(gate.evaluate(inputs[inputs_index:inputs_index + gate.inputs()]))
        inputs_index += gate.inputs()

    return result





