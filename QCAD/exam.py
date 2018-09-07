# Module for examination

from QCAD import Module, QuantumCircuit, execute
from QCAD import TypicalModule as tm

from QCAD import Backend

import numpy as np


# 주어진 Matrix가 Unitary 인지를 판별하는 함수 (나중에 쓸 수 있을지도?)
def is_unitary(matrix: np.ndarray) -> bool:

    unitary = True
    n = len(matrix)
    error = np.linalg.norm(np.eye(n) - matrix.dot( matrix.transpose().conjugate()))

    if not(error < np.finfo(matrix.dtype).eps * 10.0 *n):
        unitary = False

    return unitary


M = Module('M', 5, [tm.H[3],
                    tm.CZ[1, 2],
                    tm.Z[4]])
N = Module('N', 6, [tm.H[1],
                    M[0, 2, 3, 4, 5]])

S = Module('S', 2, [tm.CZ[1, 0]])
U = Module('U', 3, [tm.H[1]])
W = Module('W', 3, [S[0, 2],
                    U[0, 2, 1]])

print(N.typ_decompose())

qc = QuantumCircuit(N)

N_matrix = Backend.MatrixModel.get_modulematrix(N)
print(N_matrix, '\n', is_unitary(N_matrix))

print(Backend.MatrixModel.get_modulematrix(S))

print(Backend.MatrixModel.get_modulematrix(U))

W_matrix = Backend.MatrixModel.get_modulematrix(W)
print(W_matrix, '\n', is_unitary(W_matrix))

print('done')