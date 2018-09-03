# Module for class No Optimized Matrix Model (NOMM)

from .. import QuantumCircuit
from . import MatrixModel


class Nomm(MatrixModel):
    def __init__(self, quantum_circuit: QuantumCircuit):
        self.runable = True

