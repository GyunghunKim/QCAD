# Module for function execute

from . import QuantumCircuit
from . import Backend

import math
import numpy as np
import matplotlib.pyplot as plt

def execute(backend, quantum_circuit: QuantumCircuit, initial_state = [], option='', abs_tol=1e-08):
    # TODO: 무엇을 리턴할 지 생각해 보아야 함.
    
    _state_vector = [1.+0.j]
    if not initial_state:
        _state_vector = [0.+0.j] * 2 ** quantum_circuit.n
        _state_vector[0] = 1.+0.j
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

    if option == 'silent':
        return
    if option == 'nonzero':
        prob = [(x*np.conjugate(x)).real for x in _res]
        print('='*50)
        print("# : State")
        form_str = '{0:0' + str(quantum_circuit.n) + 'b}'
        for i in range(len(prob)):
            if math.isclose(prob[i], 0, abs_tol=abs_tol) is False:
                print(form_str.format(i) + f" : {_res[i]}")
        print('='*50)

    if option == 'barplot':
        plt.bar(np.arange(2 ** quantum_circuit.n), [(x*np.conjugate(x)).real for x in _res])
        plt.ylabel('Probability')
        plt.xticks(np.arange(0, 2 ** quantum_circuit.n))
        plt.ylim(bottom=0, top=1)

        plt.show()
