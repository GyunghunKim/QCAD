from . import Bit


class Register(object):
    def __init__(self, n):
        self.bits = []
        for _i in range(n):
            self.bits.append(Bit())

    def __getitem__(self, item):
        return self.bits[item]

    def __setitem__(self, key, value):
        self.bits[key] = value

    def append(self, bit):
        self.bits.append(bit)

    def __len__(self):
        return len(self.bits)
