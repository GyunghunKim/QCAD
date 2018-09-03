from QCAD import Module, QuantumCircuit, execute
from QCAD import TypicalModule as tm

from QCAD import Backend

M = Module('M', 5, [tm.H[3],
                    tm.CZ[1, 2],
                    tm.Z[4]])
N = Module('N', 6, [tm.H[1],
                    M[0, 2, 3, 4, 5]])

S = Module('S', 2, [tm.CZ[1, 0]])
U = Module('U', 3, [tm.H[1]])

print(N.typ_decompose())

qc = QuantumCircuit(N)

print(Backend.MatrixModel.get_modulematrix(N))
print(Backend.MatrixModel.get_modulematrix(S))
print(Backend.MatrixModel.get_modulematrix(U))

print('done')