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
def matrix_model():
    execute('MatrixModel', qc, option='NoPrint')

@runtime
def optimized_gate_extended():
    execute('OptimizedGate_Extended', qc,option='NoPrint')

#8 qubits = 0.3710s
#9 qubits = 2.0160s
#10 qubits = 9.8787s
#11 qubits = 67.7230s
#12 qubits = 0.0544s

if __name__ == '__main__':
    my_module = Module('M', 22, [tm.H[0]])
    qc = QuantumCircuit(my_module)

    # matrix_model()
    optimized_gate_extended()