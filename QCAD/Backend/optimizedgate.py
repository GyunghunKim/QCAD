# Module for class Optimized Matrix Model

import numpy as np

from . import Backend
from .. import Module
from .. import QuantumCircuit

class OptimizedGate(Backend):
    def __init__(self):
        pass

    @staticmethod
    def is_typical(module: Module):
        if module.n is 1:
            return True

        if module.controlled and module.n is 2:
            return True

        return False

    @staticmethod
    def is_decomposable(module: Module):
        if module.controlled or not module.sub_modules:
            return False

        return True

    @staticmethod
    def decompose(module: Module):
        class UnsupportableGateError(Exception):
            pass

        # 모듈을 기본적인 모듈(게이트)로 분해해주는 함수
        if OptimizedGate.is_decomposable(module) is False and OptimizedGate.is_typical(module) is False:
            raise UnsupportableGateError()

        _temp_sub_modules = module.sub_modules.copy()
        _temp_reg_indices = module.reg_indices.copy()

        for _i in range(len(module.reg_indices)):
            if OptimizedGate.is_typical(_temp_sub_modules[_i]) is False:
                _temp_decom = OptimizedGate.decompose(_temp_sub_modules[_i])

                del _temp_sub_modules[_i]
                for _j in range(len(_temp_decom[0])):
                    _temp_sub_modules.insert(_i+_j, _temp_decom[0][_j])

                del _temp_reg_indices[_i]
                for _k in range(len(_temp_decom[1])):
                    _temp_indices = []
                    for _l in _temp_decom[1][_k]:
                        _temp_indices.append(module.reg_indices[_i][_l])
                    _temp_reg_indices.insert(_i + _k, _temp_indices)

        return _temp_sub_modules, _temp_reg_indices

    @staticmethod
    def run(quantum_circuit: QuantumCircuit, initial_state=[]):
        _n = quantum_circuit.n
        _n_state = 2 ** _n

        _state_vector = [1]
        if not initial_state:
            _state_vector = [0.] * _n_state
            _state_vector[0] = 1.
        elif len(initial_state) is _n_state:
            _state_vector = initial_state[:]
        elif len(initial_state) is _n:
            for _state in initial_state:
                _state_vector = np.kron(_state, _state_vector)


        _modules, _indices = OptimizedGate.decompose(quantum_circuit.module)

        for _module, _index in zip(_modules, _indices):
            for i in range(_n_state):
                pass

