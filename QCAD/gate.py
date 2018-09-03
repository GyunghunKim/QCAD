from QCAD import Module, Register, Bit


class Gate(object):
    def __init__(self, reg, module):
        self.name = module.name
        self.reg = reg
        self.sub_gates = []

        for _module, _reg_index in zip(module.sub_modules, module.reg_indices):
            _temp_reg = Register(0)
            for _i in _reg_index:
                _temp_reg.append(Bit(_i))

            self.sub_gates.append(Gate(_temp_reg, _module))
