from . import QuantumCircuit
from . import Module
def qcad2qasm(qc:QuantumCircuit,option="IBM_QASM",decomposed=True):
    qc_typ_sub_modules=qc.module.typ_decompose()[0].copy()
    qc_typ_reg_indices=qc.module.typ_decompose()[1].copy()
    if(option=="IBM_QASM"):
        f=open(qc.module.name+"_qasm.txt",'w')
        f.write("OPENQASM 2.0;\ninclude \"qelib1.inc\";\n ")
        wqcbit="qreg q[%d];\ncreg c[%d];\n" % (qc.n,qc.n)
        f.write(wqcbit)
        modulenum=0
        for typ_sub_module in qc_typ_sub_modules:
            module_name=typ_sub_module.name.lower()
            data=module_name.copy()
            indnum=0
            for reg_indices in qc_typ_reg_indices[modulenum]:
                if(indnum is not 0):
                    data+=", "
                data += "q[%d]" % reg_indices[indnum]
                ++indnum
            ++modulenum
        data+=";\n"
        f.write(data)


