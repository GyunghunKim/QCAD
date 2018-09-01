class Module(object):
    def __init__(self, name, n, ind_modules=[]):
        self.name = name
        self.n = n
        self.sub_modules = []
        self.reg_indices = []

        for _ind_module in ind_modules:
            self.sub_modules.append(_ind_module[0])
            self.reg_indices.append(_ind_module[1])

    def __getitem__(self, item):
        if isinstance(item, int):
            return [self, (item,)]
        return [self, item]


class TypicalModule:
    I = Module('I', 1)
    H = Module('H', 1)
    X = Module('X', 1)
    Y = Module('Y', 1)
    Z = Module('Z', 1)
    CZ = Module('CZ', 2)

    def __init__(self):
        pass
