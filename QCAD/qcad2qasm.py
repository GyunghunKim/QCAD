from . import QuantumCircuit
from . import Module

def qcad2qasm(qc: QuantumCircuit, option='IBM_QASM', decomposed=True, to_file=True):
    output = ''
    
    qc_typ_sub_modules = qc.module.typ_decompose()[0].copy()
    qc_typ_reg_indices = qc.module.typ_decompose()[1].copy()

    print(qc_typ_reg_indices);
    print(qc_typ_sub_modules);

    if option is 'IBM_QASM':
        output += 'OPENQASM 2.0;\ninclude \"qelib1.inc\";\n\n'
        output += 'qreg q[%d];\ncreg c[%d];\n\n' % (qc.n, qc.n)

        modulenum = 0
        for module_num, typ_sub_module in zip(range(len(qc_typ_sub_modules)), qc_typ_sub_modules):
            module_name = typ_sub_module.name.lower()
            output += module_name + ' '
            indnum = 0
            for reg_index in qc_typ_reg_indices[module_num]:
                output += 'q[%d], ' % reg_index
                indnum += 1
            output += '\b\b;\n'
        
        for i in range(qc.n):
            output += 'measure q[%d]->c[%d];\n' % (i, i)

    if to_file:
        f = open(qc.module.name+'_qasm.txt', 'w')
        f.write(output)
        f.close()
    else:
        return output
