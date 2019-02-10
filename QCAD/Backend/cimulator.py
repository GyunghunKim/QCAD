# Module for simulator developed with C++

import numpy as np
import math
import os

from ctypes import *
# from numpy.ctypeslib import ndpointer

from . import Backend
from . import MatrixModel
from .. import TypicalModule
from .. import QuantumCircuit

class Cimulator(Backend):
    def __init__(self):
        pass

    @staticmethod
    def run(quantum_circuit: QuantumCircuit, state_vector):
        
        csim = cdll.LoadLibrary('%s/csim.so' % os.path.dirname(os.path.realpath(__file__)))

        csim.resetQC()

        csim.setNumQubit(quantum_circuit.n)

        for _gate, _indices in zip(*quantum_circuit.module.typ_decompose()):
           Cimulator.sendGateToBackend(csim, _gate, _indices)

        csim.printQCStatus()

        _c_state_real, _c_state_imag = [(c_double * len(x))(*x) for x in
            [np.real(state_vector).tolist(), np.imag(state_vector).tolist()]]

        csim.run.restype = POINTER(c_double * (2 * (2**quantum_circuit.n)))
        _c_res_state = csim.run(_c_state_real, _c_state_imag).contents

        _res_state = [0] * (2**quantum_circuit.n)
        for i in range(2**quantum_circuit.n):
            _res_state[i] = complex(_c_res_state[i], _c_res_state[i+2**quantum_circuit.n])

        return _res_state

    @staticmethod
    def sendGateToBackend(handle, module, indices):
        if module.typical is not True:
            print("Exception")

        _targets = list()
        _controls = list()

        if module.controlled is True:
            _c_name = c_char_p(module.name.encode('ascii'))
            for _index in module.reg_indices[0]:
                _targets.append(indices[_index])
            for _index in module.control_bits:
                _controls.append(indices[_index])

            _c_targets = (c_int * len(_targets))(*_targets)
            _c_controls = (c_int * len(_controls))(*_controls)
            _c_matrix_real, _c_matrix_imaginary = [(c_double * len(x))(*x) for x in
                Cimulator.getModuleMatrixIn1D(module.sub_modules[0], option='separated')]

            handle.addGate(_c_name, _c_matrix_real, _c_matrix_imaginary,
                    True, len(_targets), _c_targets, len(_controls), _c_controls)

        else:
            _c_name = c_char_p(module.name.encode('ascii'))
            for _index in indices:
                _targets.append(_index)

            _c_targets = (c_int * len(_targets))(*_targets)
            _c_matrix_real, _c_matrix_imaginary = [(c_double * len(x))(*x) for x in
                Cimulator.getModuleMatrixIn1D(module, option='separated')]

            handle.addGate(_c_name, _c_matrix_real, _c_matrix_imaginary,
                    False, len(_targets), _c_targets, 0, None)

    @staticmethod
    def getModuleMatrixIn1D(module, option=''):
        _matrix = MatrixModel.get_modulematrix(module)
        _matrix_in_1d = np.reshape(_matrix, (1, -1))
        
        if option == '':
            return _matrix_in_1d[0].tolist()
        if option == 'separated':
            return _matrix_in_1d[0].real.tolist(), _matrix_in_1d[0].imag.tolist()
