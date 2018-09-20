# Module for function execute

from . import QuantumCircuit
from . import Backend

import numpy as np
import matplotlib.pyplot as plt

def execute(backend, quantum_circuit: QuantumCircuit, initial_state = []):
    # TODO: 무엇을 리턴할 지 생각해 보아야 함.

    # No Optimized Matrix Model
    if backend is "MatrixModel":
        _res = Backend.MatrixModel.run(quantum_circuit, initial_state)
        print(_res)

        plt.bar(np.arange(2 ** quantum_circuit.n), [(x*np.conjugate(x))[0].real for x in _res])
        plt.ylabel('Probability')
        plt.xticks(np.arange(0, 2 ** quantum_circuit.n))
        plt.ylim(bottom=0, top=1)

        plt.show()
