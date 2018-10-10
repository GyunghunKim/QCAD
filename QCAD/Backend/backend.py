# Module for class Backend

from .. import QuantumCircuit

class Backend(object):
    def __init__(self):
        pass

    @staticmethod
    def run(quantum_circuit: QuantumCircuit, initial_state=[]):
        ...
