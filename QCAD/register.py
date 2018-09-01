from . import Bit


class Register(object):
    def __init__(self, n):
        self.bits = []
        for _i in range(n):
            self.bits.append(Bit())

    def __getitem__(self, item):
        return self.bits[item]

    def append(self, bit):
        self.bits.append(bit)
