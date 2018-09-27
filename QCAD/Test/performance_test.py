from QCAD import Module, QuantumCircuit, execute
from QCAD import TypicalModule as tm

def runtime(f):
    def wrapper():
        import timeit
        start = timeit.default_timer()
        f()
        end = timeit.default_timer()
        print(f'Elapsed Time: {end-start:.4f}s')
        return
    return wrapper


@runtime
def n_qubit_gate():
    my_module = Module('M', 11, [tm.H[0],
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

    execute('MatrixModel', qc, option='NoPrint')

#8 qubits = 0.3710s
#9 qubits = 2.0160s
#10 qubits = 9.8787s
#11 qubits = 67.7230s
#12 qubits = 537.9753s

if __name__ == '__main__':
    n_qubit_gate()