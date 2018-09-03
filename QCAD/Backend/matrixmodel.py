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
    TypicalMatrix = {'H':H, 'X':X, 'Y':Y, 'Z':Z, 'I':I, 'T':T, 'CZ':CZ}

    def __init__(self, quantum_circuit):
        pass

    @staticmethod
    def get_gatematrix(gate):
        """
        :param gate: 게이트 객체를 전달
        :return: 게이트를 매트릭스로 반환
        """
        if not gate.sub_gates:
            return MatrixModel.TypicalMatrix[gate.name]

        _gate_matrix = np.eye(2 ** len(gate.reg), dtype='complex')

        for _sub_gate in gate.sub_gates:
            _apply_list = []
            for _bit in _sub_gate.reg.bits:
                _apply_list.append(_bit.data)

            _permute_matrix = np.eye(2 ** len(gate.reg), dtype='complex')
            for _i, _j in zip(range(len(_apply_list)), _apply_list):
                _permute_matrix[[_i, _j]] = _permute_matrix[[_j, _i]]

            _temp_gate_matrix = MatrixModel.get_gatematrix(_sub_gate)
            for _i in range(len(gate.reg) - len(_apply_list)):
                _temp_gate_matrix = np.kron(MatrixModel.TypicalMatrix['I'], _temp_gate_matrix)

            _sub_gate_matrix = _permute_matrix @ _temp_gate_matrix @ _permute_matrix

            _gate_matrix = _sub_gate_matrix @ _gate_matrix

        return _gate_matrix
