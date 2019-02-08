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
#            for _ind_module1 in range(len(_ind_module[1])):
#                if not _ind_module[1][_ind_module1] < self.n:
#                    raise IndexError

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
        if self.typical is True:
            return [self], [list(range(self.n))]

        _res_sub_modules = list()
        _res_reg_indices = list()

        for _sub_module, _reg_index in zip(self.sub_modules, self.reg_indices):
            _decomp_sub_modules, _decomp_reg_indices = _sub_module.typ_decompose()

            for _decomp_sub_module, _decomp_reg_index in zip(_decomp_sub_modules, _decomp_reg_indices):
                _res_sub_modules.append(_decomp_sub_module)
                _temp_index = list()
                for i in _decomp_reg_index:
                    _temp_index.append(_reg_index[i])
                _res_reg_indices.append(_temp_index)

        return _res_sub_modules, _res_reg_indices

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
            if self.typical is True:
                return [self], [list(range(self.n))]

            _res_sub_modules = list()
            _res_reg_indices = list()

            for _sub_module, _reg_index in zip(self.sub_modules, self.reg_indices):
                _decomp_sub_modules, _decomp_reg_indices = _sub_module.typ_decompose()

                for _decomp_sub_module, _decomp_reg_index in zip(_decomp_sub_modules, _decomp_reg_indices):
                    _temp_index = list()
                    _temp_index.extend(self.control_bits)
                    for i in _decomp_reg_index:
                        _temp_index.append(_reg_index[i])
                    
                    _temp_sub_mcu_name = _decomp_sub_module.name
                    _temp_sub_mcu_n = _decomp_sub_module.n + len(self.control_bits)
                    _temp_reg_index = list()

                    if _decomp_sub_module.controlled is False:
                        _temp_sub_mcu_control_bits = list(range(len(self.control_bits)))
                        for i in _decomp_reg_index:
                            _temp_reg_index = list(range(len(self.control_bits), _temp_sub_mcu_n))
                        _temp_sub_mcu_applied_module = [_decomp_sub_module, _temp_reg_index]

                    else:
                        _temp_sub_mcu_control_bits = list(range(len(self.control_bits)+len(_decomp_sub_module.control_bits)))
                        _temp_reg_index = list(range(len(_temp_sub_mcu_control_bits), _temp_sub_mcu_n))
                        _temp_sub_mcu_applied_module = [_decomp_sub_module.sub_modules[0], _temp_reg_index]

                    _temp_sub_mcu = TypicalModule.MCU(_temp_sub_mcu_name, _temp_sub_mcu_n,
                            _temp_sub_mcu_control_bits, _temp_sub_mcu_applied_module)
                    _temp_sub_mcu.set_typical(True)

                    _res_sub_modules.append(_temp_sub_mcu)
                    _res_reg_indices.append(_temp_index)

            return _res_sub_modules, _res_reg_indices

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
