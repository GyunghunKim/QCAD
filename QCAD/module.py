# Module of class Module (Quantum Gates)
import numpy as np

import copy

class Module(object):
    def __init__(self, name, n, ind_modules=[]):
        # initialize
        self.name = name
        self.n = n
        self.sub_modules = []
        self.reg_indices = []
        self.typical = False
        self.matrix_only_defined = False
        self.controlled = False

        for _ind_module in ind_modules:
            self.sub_modules.append(_ind_module[0])
            self.reg_indices.append(_ind_module[1])
            for _ind_module1 in range(len(_ind_module[1])):
                if not _ind_module[1][_ind_module1] < self.n:
                    raise IndexError

    def show(self):
        print(f'Name        :{self.name}')
        print(f'N           :{self.n}')
        print(f'sub_modules :{self.sub_modules}')
        print(f'reg_indices :{self.reg_indices}')
        print(f'typical     :{self.typical}')
        print(f'contolled   :{self.controlled}')

    def set_typical(self, typical):
        self.typical = typical

    def __getitem__(self, item):
        if isinstance(item, int):
            if self.n != 1:
                raise RegisterMatchError()
            return [self, [item]]

        if len(item) is not self.n:
            raise RegisterMatchError()

        return [self, list(item)]

    def get_submodules(self):
        #모듈의 sub_modules의 정보를 얻는 함수
        return self.sub_modules, self.reg_indices

    def typ_decompose(self):
        # 모듈을 기본적인 모듈(게이트)로 분해해주는 함수
        temp_sub_modules = self.sub_modules.copy()
        temp_reg_indices = self.reg_indices.copy()

        for i in range(len(self.reg_indices)):
            if temp_sub_modules[i].typical is False:
                temp_decom = temp_sub_modules[i].typ_decompose()

                del temp_sub_modules[i]
                for j in range(len(temp_decom[0])):
                    temp_sub_modules.insert(i+j, temp_decom[0][j])

                del temp_reg_indices[i]
                for k in range(len(temp_decom[1])):
                    temp_indices = [] 
                    for l in temp_decom[1][k]:
                        temp_indices.append(self.reg_indices[i][l])
                    temp_reg_indices.insert(i + k, temp_indices)

        return temp_sub_modules, temp_reg_indices


class TypicalModule:
    class U(Module):
        def __init__(self, name, n, matrix):
            super().__init__(name, n)
            self.matrix_only_defined = True
            self.matrix = np.array(matrix)
            self.set_typical(True)

    class MCU(Module):
        def __init__(self, name, n, control_bits, applied_module):
            # TODO: applied_module이 1개 이상 들어오는 경우 에러 처리 필요

            super().__init__(name, n, [applied_module])
            self.controlled = True
            self.control_bits = sorted(control_bits)

        def typ_decompose(self):
            _temp_self = copy.deepcopy(self)
            _sub_modules, _reg_indices = super().typ_decompose()

            _port_indices = list()
            _sub_mcus = list()
            for _sub_module, _reg_index in zip(_sub_modules, _reg_indices):

                _core_module = _sub_module

                if _sub_module.controlled is True:
                    for _sub_control_bit in _sub_module.control_bits:
                        _temp_self.control_bits.append(_reg_index[_sub_control_bit])
                    for _sub_control_bit in sorted(_sub_module.control_bits,
                            reverse=True):
                        del _reg_index[_sub_control_bit]
                    _core_module = _sub_module.sub_modules[0]
                _temp_n = len(_temp_self.control_bits) + len(_reg_index)

                _temp_port_index = list(_temp_self.control_bits)
                _temp_port_index.extend(_reg_index)

                _temp_mcu = TypicalModule.MCU(_temp_self.name, _temp_n,
                        list(range(len(_temp_self.control_bits))),
                        [_core_module, list(range(len(_temp_self.control_bits),
                            _temp_n))])
                _temp_mcu.set_typical(True)
                _sub_mcus.append(_temp_mcu)

                _port_indices.append(_temp_port_index)

            return _sub_mcus, _port_indices

        def show(self):
            super().show()
            print(f'control_bits  :{self.control_bits}')

    class RX(U):
        def __init__(self, name, theta):
            super().__init__(name, 1, [[np.cos(theta/2), -np.sin(theta/2)*1.j],
                [-np.sin(theta/2)*1.j, np.cos(theta/2)]])
            self.name = name
            self.set_typical(True)

    class RY(U):
        def __init__(self, name, theta):
            super().__init__(name, 1, [[np.cos(theta/2), -np.sin(theta/2)],
                [np.sin(theta/2), np.cos(theta/2)]])
            self.name = name
            self.set_typical(True)

    class RZ(U):
        def __init__(self, name, theta):
            super().__init__(name, 1, [[np.cos(theta/2)-np.sin(theta/2)*1.j, 0],
                [0, np.cos(theta/2)+np.sin(theta/2)*1.j]])
            self.name = name
            self.set_typical(True)

    I = Module('I', 1)
    H = Module('H', 1)
    X = Module('X', 1)
    Y = Module('Y', 1)
    Z = Module('Z', 1)
    T = Module('T', 1)
    S = Module('S', 1)
    CX = MCU('CX', 2, [0], X[1])
    CZ = MCU('CZ', 2, [0], Z[1])
    CCX = MCU('CCX', 3, [0, 1], X[2])
    CCZ = MCU('CCZ', 3, [0, 1], Z[2])

    I.set_typical(True)
    H.set_typical(True)
    X.set_typical(True)
    Y.set_typical(True)
    Z.set_typical(True)
    T.set_typical(True)
    S.set_typical(True)

    def __init__(self):
        pass



class RegisterMatchError(Exception):
    pass

class MCUModuleTypeError(Exception):
    pass
