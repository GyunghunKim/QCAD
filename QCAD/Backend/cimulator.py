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

        _gates = quantum_circuit.module.typ_decompose()
        for (_gate, _indices) in zip(_gates[0], _gates[1]):
           pass 
        #    _ Cimulator.sendGateToBackend(_gate, _indices)
        #    _num_target = len(_indices)
        #    _c_index_array = (c_int * len(_indices))(*_indices)
        #    _gate_name = _gate.name

        #    csim.addGate(_gate_name, _c_index_array, _num_target)

        csim.printQCStatus()

        csim.run()

        return []

#    @staticmethod
#    def sendGateToBackend(module: Module, indices):


