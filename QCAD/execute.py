# Module for function execute

from . import QuantumCircuit
from . import Backend

import numpy as np
import matplotlib.pyplot as plt

def execute(backend, quantum_circuit: QuantumCircuit, initial_state = [], option=''):
    # TODO: 무엇을 리턴할 지 생각해 보아야 함.
    
    _state_vector = [1]
    if not initial_state:
        _state_vector = [0.] * 2 ** quantum_circuit.n
        _state_vector[0] = 1.
    elif len(initial_state) is 2 ** quantum_circuit.n:
        _state_vector = initial_state[:]
    elif len(initial_state) is quantum_circuit.n:
        for _state in initial_state:
            _state_vector = np.kron(_state, _state_vector)

    # No Optimized Matrix Model
    if backend == "MatrixModel":
        _res = Backend.MatrixModel.run(quantum_circuit, _state_vector)
    
    # Optimized C++ Matrix Model
    if backend == "Cimulator":
        _res = Backend.Cimulator.run(quantum_circuit, _state_vector)

    if option == "NoPrint":
        return

    print(_res)

    plt.bar(np.arange(2 ** quantum_circuit.n), [(x*np.conjugate(x)).real for x in _res])
    plt.ylabel('Probability')
    plt.xticks(np.arange(0, 2 ** quantum_circuit.n))
    plt.ylim(bottom=0, top=1)

    plt.show()
