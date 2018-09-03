from QCAD import Module,Register, QuantumCircuit
from QCAD import TypicalModule as tm

M = Module('M', 5, [tm.H[3],
                    tm.CZ[1, 2],
                    tm.Z[4]])
N = Module('N', 6, [tm.H[1],
                    M[0, 2, 3, 4, 5]])

print(N.typ_decompose())

reg = Register(6)
qc = QuantumCircuit(reg,N)
print('done')