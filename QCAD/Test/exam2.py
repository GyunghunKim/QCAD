from QCAD import Module, QuantumCircuit, execute, circuit_drawer
from QCAD import TypicalModule as tm

from QCAD.Backend import MatrixModel, OptimizedGate, OptimizedGateExtended

import numpy as np

if __name__ == '__main__':
    rx_half_pi = tm.RX(np.pi/2)

    custom_u = tm.U(2, [[-1, 0], [0, 1]])

    multi_control_h = tm.MCU(3, [0, 1], tm.H[2])

    my_module = Module('M', 4, [tm.H[0],
                                tm.H[1],
                                tm.H[2],
                                tm.H[3],
                                tm.CX[3, 2],
                                tm.Y[1],
                                tm.Z[2],
                                tm.H[0],
                                tm.T[1],
                                tm.T[2],
                                tm.CX[3, 2],
                                tm.CX[2, 0]])

    N = Module('N', 5, [my_module[1, 2, 4, 3],
                        tm.H[0],
                        tm.U(1, [[1, 0],
                                 [0, 1]])[1]])

    qc = QuantumCircuit(my_module)

    l = qc.module.typ_decompose()

    # print(OptimizedGateExtended.decompose(N)[1])
    # module_matrices = []
    # for module in OptimizedGateExtended.decompose(N)[0]:
    #     module_matrices.append(MatrixModel.get_modulematrix(module))
    # print(module_matrices)

    execute('MatrixModel', qc)
    execute('OptimizedGate_Extended', qc)