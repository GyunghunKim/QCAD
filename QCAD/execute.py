# Module for function execute

from . import QuantumCircuit
from . import Backend


def execute(backend, quantum_circuit: QuantumCircuit, initial_state):
    # TODO: 무엇을 리턴할 지 생각해 보아야 함.

    # No Optimized Matrix Model
    if backend is "MatrixModel":
        Backend.MatrixModel.run(quantum_circuit, initial_state)
