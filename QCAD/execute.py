# Module for function execute

from . import QuantumCircuit
from . import Backend


def execute(quantum_circuit: QuantumCircuit, backend):
    # TODO: 무엇을 리턴할 지 생각해 보아야 함.

    # No Optimized Matrix Model
    if backend is "NOMM":
        Backend.Nomm(quantum_circuit)

    # Cuda Optimized Matrix Model
    if backend is "COMM":
        Backend.Comm(quantum_circuit)
