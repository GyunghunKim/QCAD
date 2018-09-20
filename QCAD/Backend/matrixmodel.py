# Module for class Matrix Model

import numpy as np
import math
from copy import deepcopy

from . import Backend
from .. import TypicalModule
from .. import QuantumCircuit


class MatrixModel(Backend):
    H = np.multiply(0.5 ** 0.5, [[1., 1.],
                                 [1., -1.]])
    X = [[0., 1.],
         [1., 0.]]
    Y = [[0., -1.j],
         [1.j, 0.]]
    Z = [[1., 0.],
         [0., -1.]]
    I = [[1., 0.],
         [0., 1.]]
    T = [[1., 0.],
         [0., np.exp(math.pi / 4 * 1.0j)]]
    CX = [[1., 0., 0., 0.],
          [0., 1., 0., 0.],
          [0., 0., 0., 1.],
          [0., 0., 1., 0.]]
    CZ = [[1., 0., 0., 0.],
          [0., 1., 0., 0.],
          [0., 0., 1., 0.],
          [0., 0., 0., -1.]]

    #TypicalMatrix dictionary는 알려진 모듈의 이름과 행렬을 관계지음.
    PreDefinedModeules = {'H':H, 'X':X, 'Y':Y, 'Z':Z, 'I':I, 'T':T, 'CX':CX, 'CZ':CZ}

    def __init__(self):
        pass

    @staticmethod
    def get_modulematrix(module):
        # 모듈을 받아서 행렬로 바꿔주는 함수
        # TODO: 최적화 가능한 알고리즘이므로 추가적인 개발 필요.

        if module.name in MatrixModel.PreDefinedModeules:
            return MatrixModel.PreDefinedModeules[module.name]

        elif module.matrix_only_defined is True:
            return module.matrix

        elif module.controlled is True:
            return MatrixModel.get_controlled_modulematrix(module)

        else:
            _module_matrix = np.eye(2 ** module.n, dtype='complex')

            for _sub_module, _index in zip(module.sub_modules, module.reg_indices):

                # _index에 들어있는 값들에 해당하는 permutation matrix를 구한다.
                _permutation_matrix = np.eye(2 ** module.n)

                _temp_array = list(range(module.n))

                for _i in range(len(_index)):
                    if _temp_array[_i] is not _index[_i]:
                        _a, _b = _i, _temp_array.index(_index[_i])
                        _temp_array[_b], _temp_array[_a] = _temp_array[_a], _temp_array[_b]
                        _permutation_matrix = MatrixModel.get_permutationmatrix(module.n, _a,
                                                                                _b) @ _permutation_matrix

                _temp_module_matrix = MatrixModel.get_modulematrix(_sub_module)

                for _i in range(module.n - len(_index)):
                    _temp_module_matrix = np.kron(MatrixModel.PreDefinedModeules['I'], _temp_module_matrix)

                # 모듈의 matrix를 구한다.
                _sub_module_matrix = np.linalg.inv(_permutation_matrix) @ _temp_module_matrix @ _permutation_matrix

                _module_matrix = _sub_module_matrix @ _module_matrix

                return _module_matrix

    @staticmethod
    def get_controlled_modulematrix(module: TypicalModule.MCU):
        # 재귀적 처리를 통해 MCU의 행렬 표현을 구한다.
        _module = deepcopy(module)

        if not module.control_bits:
            _module.controlled = False
            return MatrixModel.get_modulematrix(_module)

        _permutation_matrix = np.eye(2 ** _module.n)

        if 0 not in _module.control_bits:
            _a = _module.control_bits[0]
            _module.control_bits[0] = 0

            if 0 in _module.reg_indices[0]:
                _module.reg_indices[0][_module.reg_indices[0].index(0)] = _a

            _permutation_matrix = MatrixModel.get_permutationmatrix(_module.n, 0, _a)

        _module.control_bits.remove(0)
        _module.n -= 1
        _module.control_bits[:] = [x - 1 for x in _module.control_bits]
        _module.reg_indices[0][:] = [x - 1 for x in _module.reg_indices[0]]

        _dim = 2 ** _module.n
        return np.linalg.inv(_permutation_matrix) \
               @ np.block([[np.eye(_dim), np.zeros((_dim, _dim))],
                           [np.zeros((_dim, _dim)), MatrixModel.get_controlled_modulematrix(_module)]]) \
               @ _permutation_matrix


    @staticmethod
    def get_permutationmatrix(n, i, j):
        # n-qubit system에서 i번째 qubit과 j번째 qubit의 permutation을 나타내는 행렬을 반환
        if i is j:
            return np.eye(2 ** n)
        
        _permutation_matrix_array = [np.array([[1]])] * 4
        
        for _k in range(n):
            if _k in (i, j):
                _permutation_matrix_array[0] = np.kron(np.array([[1, 0], [0, 0]]), _permutation_matrix_array[0])
                _permutation_matrix_array[1] = np.kron(np.array([[0, 0], [0, 1]]), _permutation_matrix_array[1])
                if _k is i:
                    _c1 = 1
                    _c2 = 0
                else:
                    _c1 = 0
                    _c2 = 1
                _permutation_matrix_array[2] = np.kron(np.array([[0, _c1], [_c2, 0]]), _permutation_matrix_array[2])
                _permutation_matrix_array[3] = np.kron(np.array([[0, _c2], [_c1, 0]]), _permutation_matrix_array[3])
            else:
                for _l in range(len(_permutation_matrix_array)):
                    _permutation_matrix_array[_l] = np.kron(np.eye(2), _permutation_matrix_array[_l])

        _temp_permutation_matrix = sum(_permutation_matrix_array)

        return _temp_permutation_matrix

    @staticmethod
    def run(quantum_circuit: QuantumCircuit, initial_state=[]):
        # initial_state를 받아서 circuit을 계산한 뒤 결과를 리턴한다.
        _state_vector = [1]
        if not initial_state:
            _state_vector = [0.] * 2 ** quantum_circuit.n
            _state_vector[0] = 1.
        elif len(initial_state) is 2 ** quantum_circuit.n:
            _state_vector = initial_state[:]
        elif len(initial_state) is quantum_circuit.n:
            for _state in initial_state:
                _state_vector = np.kron(_state, _state_vector)

        _state_vector = np.array([_state_vector]).T

        _result = MatrixModel.get_modulematrix(quantum_circuit.module) @ _state_vector

        return _result