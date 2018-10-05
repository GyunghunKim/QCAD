import numpy as np

from . import Backend, MatrixModel
from .. import Module
from .. import QuantumCircuit

class OptimizedGateExtended(Backend):
    @staticmethod
    def is_decomposable(module: Module):
        if module.controlled or not module.sub_modules:
            return False

        return True

    @staticmethod
    def decompose(module: Module):
        # 모듈을 기본적인 모듈(게이트)로 분해해주는 함수

        class UnsupportableGateError(Exception):
            pass

        temp_sub_modules = module.sub_modules.copy()
        temp_reg_indices = module.reg_indices.copy()

        for i in range(len(module.reg_indices)):
            if OptimizedGateExtended.is_decomposable(temp_sub_modules[i]) is True:
                temp_decom = OptimizedGateExtended.decompose(temp_sub_modules[i])

                del temp_sub_modules[i]
                for j in range(len(temp_decom[0])):
                    temp_sub_modules.insert(i + j, temp_decom[0][j])

                del temp_reg_indices[i]
                for k in range(len(temp_decom[1])):
                    temp_indices = []
                    for l in temp_decom[1][k]:
                        temp_indices.append(module.reg_indices[i][l])
                    temp_reg_indices.insert(i + k, temp_indices)

        return temp_sub_modules, temp_reg_indices

    @staticmethod
    def get_mapped_index(index, n, j, i):
        # map index from n-state vector to len(index)-state vector, j is key and i is trash
        _bin = [-1] * n
        for _i in range(len(index)):
            _bin[n-index[_i]-1] = (j & (1 << _i)) >> _i

        _i = 0
        for _j in range(n):
            if _bin[_j] is -1:
                _bin[_j] = (i & (1 << _i)) >> _i
                _i += 1

        _out = 0
        for _bit in _bin:
            _out = (_out << 1) | _bit

        return _out

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

        _modules, _indices = OptimizedGateExtended.decompose(quantum_circuit.module)
        _module_matrices = []
        for _module in _modules:
            _module_matrices.append(MatrixModel.get_modulematrix(_module))

        for _module_matrix, _index in zip(_module_matrices, _indices):
            for _i in range(2**(_n-len(_index))):
                _ind_map = []
                _state_mini = []
                for _j in range(2**len(_index)):
                    _ind_map.append(OptimizedGateExtended.get_mapped_index(_index, _n, _j, _i))
                    _state_mini.append(_state_vector[_ind_map[_j]])

                _state_mini = np.matmul(_module_matrix, _state_mini)

                for _j in range(2**len(_index)):
                    _state_vector[_ind_map[_j]] = _state_mini[_j]

        return _state_vector
