from QCAD import Module, QuantumCircuit, qcad2qasm
from QCAD import TypicalModule as tm

M = Module('M', 5, [tm.H[3], tm.CX[1, 2], tm.CZ[3, 1], tm.X[4], tm.T[0]])

qc = QuantumCircuit(M)

qcad2qasm(qc)
