# Module for class Matrix Model

import numpy as np
import math
from copy import deepcopy

from . import Backend
from .. import TypicalModule
from .. import Module


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
    S = [[1., 0.],
         [0., 1.0j]]
    CX = [[1., 0., 0., 0.],
          [0., 1., 0., 0.],
          [0., 0., 0., 1.],
          [0., 0., 1., 0.]]
    CZ = [[1., 0., 0., 0.],
          [0., 1., 0., 0.],
          [0., 0., 1., 0.],
          [0., 0., 0., -1.]]

    #TypicalMatrix dictionary는 알려진 모듈의 이름과 행렬을 관계지음.
    PreDefinedModeules = {'H':H, 'X':X, 'Y':Y, 'Z':Z, 'I':I, 'T':T, 'S':S, 'CX':CX, 'CZ':CZ}

    def __init__(self):
        pass

    @staticmethod
    def bit_to_int(mask):
        res = 0
        
        for i in range(len(mask)):
            res += mask[i] * (2 ** i)

        return res

    @staticmethod
    def sub_get_points(points, mask, module, reg_index, ind):
        if ind == len(reg_index):
            points.append(MatrixModel.bit_to_int(mask))
            return
        mask[reg_index[-ind-1]] = 0
        MatrixModel.sub_get_points(points, mask, module, reg_index, ind+1)
        mask[reg_index[-ind-1]] = 1
        MatrixModel.sub_get_points(points, mask, module, reg_index, ind+1)
        mask[reg_index[-ind-1]] = -1

    @staticmethod
    def sub_gate_matrix_multiplicate(points, state, module):
        temp = list()
        for i in range(len(points)):
            temp.append(state[points[i]])
        temp = np.reshape(temp, (-1, 1))
        temp = MatrixModel.get_typ_module_matrix(module) @ temp
   
        for i in range(len(points)):
            state[points[i]] = temp[i][0]

    @staticmethod
    def get_typ_module_matrix(module):
        if module.matrix_only_defined:
            return module.matrix
        if module.controlled is True:
            return MatrixModel.get_typ_module_matrix(module.sub_modules[0])
        return MatrixModel.PreDefinedModeules[module.name]

    @staticmethod
    def sub_get_mask(mask, ind, state, module, reg_index):
        if ind >= len(mask):
            points = list()
            MatrixModel.sub_get_points(points, mask, module, reg_index, 0)
            MatrixModel.sub_gate_matrix_multiplicate(points, state, module)
            return

        while mask[ind] == -1 or mask[ind] == 1:
            ind = ind+1
            if ind >= len(mask):
                MatrixModel.sub_get_mask(mask, ind, state, module, reg_index)
                return
                
        if ind < len(mask):
            MatrixModel.sub_get_mask(mask, ind+1, state, module, reg_index)
            mask[ind] = 1
            MatrixModel.sub_get_mask(mask, ind+1, state, module, reg_index)
            mask[ind] = 0

    @staticmethod
    def apply_gate(n, state, module, reg_index, control_index):
        mask = [0] * n
        for i in reg_index:
            mask[i] = -1
        for i in control_index:
            mask[i] = 1

        MatrixModel.sub_get_mask(mask, 0, state, module, reg_index)
    
    @staticmethod
    def run(quantum_circuit: Module, state_vector):
        # initial_state를 받아서 circuit을 계산한 뒤 결과를 리턴한다.
        _state_vector = state_vector.copy()

        for module, reg_index in zip(*quantum_circuit.typ_decompose()):
            temp_reg_index = list()
            temp_control_index = list()
            if module.controlled:
                for i in module.reg_indices[0]:
                    temp_reg_index.append(reg_index[i])
                for i in module.control_bits:
                    temp_control_index.append(reg_index[i])
            else:
                temp_reg_index = reg_index.copy()
        
            MatrixModel.apply_gate(quantum_circuit.n, _state_vector, module, temp_reg_index, temp_control_index)

        return _state_vector
