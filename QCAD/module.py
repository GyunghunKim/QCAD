from . import Gate
from . import Register


class Module(object):
    def __init__(self, name, n, ind_modules=[]):
        self.name = name
        self.n = n
        self.sub_modules = []
        self.reg_indices = []

        for _ind_module in ind_modules:
            self.sub_modules.append(_ind_module[0])
            self.reg_indices.append(_ind_module[1])

    def get_gate(self, reg):
        _gate = Gate(self.name, reg)

        for _module, _reg_index in zip(self.sub_modules, self.reg_indices):
            _temp_reg = Register(_module.get_reg_number())
            for _i in _reg_index:
                _temp_reg.append(reg[_i])

            _gate.add(_module.get_gate(_temp_reg))

        return _gate

    def get_reg_number(self):
        return self.n

    def __getitem__(self, *item):
        return [self, item]


class TypicalModule:
    H = Module('H', 1)

    def __init__(self):
        pass
