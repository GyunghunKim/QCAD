# Module for simulator developed with C++

import numpy as np
import math
import os

from ctypes import *
from numpy.ctypeslib import ndpointer

from . import Backend
from .. import TypicalModule
from .. import QuantumCircuit

class Cimulator(Backend):
    def __init__(self):
        pass

    @staticmethod
    def run(quantum_circuit: QuantumCircuit, initial_state=[]):
        
        csim = cdll.LoadLibrary('%s/csim.so' % os.path.dirname(os.path.realpath(__file__)))

        csim.resetQC()

        csim.setNumQubit(quantum_circuit.n)
        
        for _gate, _indices in zip(*quantum_circuit.module.typ_decompose()):
            Cimulator.sendGateToBackend(csim, _gate, _indices)
        #    _ Cimulator.sendGateToBackend(_gate, _indices)
        #    _num_target = len(_indices)
        #    _c_index_array = (c_int * len(_indices))(*_indices)
        #    _gate_name = _gate.name

        #    csim.addGate(_gate_name, _c_index_array, _num_target)

        # csim.printQCStatus()

        # csim.run()

        return []

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

            handle.addGate(_c_name, True, len(_targets),
                    _c_targets, len(_controls), _c_controls)

        else:
            _c_name = c_char_p(module.name.encode('ascii'))
            for _index in indices:
                _targets.append(_index)

            _c_targets = (c_int * len(_targets))(*_targets)

            handle.addGate(_c_name, False, len(_targets),
                    _c_targets, 0, None)
