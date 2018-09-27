from QCAD import Module, QuantumCircuit, execute, circuit_drawer
from QCAD import TypicalModule as tm

import numpy as np

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

qc = QuantumCircuit(my_module)

circuit_drawer(qc)

execute('MatrixModel', qc)