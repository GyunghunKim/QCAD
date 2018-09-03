"""
Module matrixmodel for class MatrixModel (matrix model)
Author: Gyunghun Kim
Date:   2018.09.01
"""

from . import Backend
import numpy as np
import math


class MatrixModel(Backend):
    """
    Class MatrixModel
    """
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
    CZ = [[1., 0., 0., 0.],
          [0., 1., 0., 0.],
          [0., 0., 0., 1.],
          [0., 0., 1., 0.]]

    #TypicalMatrix dictionary는 알려진 모듈의 이름과 행렬을 관계지음.
    TypicalMatrix = {'H':H, 'X':X, 'Y':Y, 'Z':Z, 'I':I, 'T':T, 'CZ':CZ}

    def __init__(self, quantum_circuit):
        pass

    @staticmethod
    def get_modulematrix(module):
        # 모듈을 받아서 행렬로 바꿔주는 함수
        # TODO: 최적화 가능한 알고리즘이므로 추가적인 개발 필요.

        if module.typical is True:
            return MatrixModel.TypicalMatrix[module.name]

        _module_matrix = np.eye(2 ** len(module), dtype='complex')

        # _index에 들어있는 값들에 해당하는 permutation matrix를 구한다.
        for _sub_module, _index in zip(module.sub_modules, module.reg_indices):
            _permutation_matrix = np.eye(2 ** len(module))

            _temp_array = list(range(len(module)))
            for _i in range(len(_index)):
                if _temp_array[_i] is not _index[_i]:
                    _a, _b = _i, _temp_array.index(_index[_i])
                    _temp_array[_b], _temp_array[_a] = _temp_array[_a], _temp_array[_b]
                    _permutation_matrix = MatrixModel.get_permutationmatrix(len(module), _a, _b) @ _permutation_matrix

            _temp_module_matrix = MatrixModel.get_modulematrix(_sub_module)
            for _i in range(len(module) - len(_index)):
                _temp_module_matrix = np.kron(MatrixModel.TypicalMatrix['I'], _temp_module_matrix)

            # 모듈의 matrix를 구한다.
            _sub_module_matrix = np.linalg.inv(_permutation_matrix) @ _temp_module_matrix @ _permutation_matrix

            _module_matrix = _sub_module_matrix @ _module_matrix

        return _module_matrix

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

