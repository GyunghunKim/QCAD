class Gate(object):
    def __init__(self, name, reg):
        self.name = name
        self.reg = reg
        self.sub_gates = []

    def add(self, gate):
        self.sub_gates.append(gate)
