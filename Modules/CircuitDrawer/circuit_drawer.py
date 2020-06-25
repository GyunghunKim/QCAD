import os
from subprocess import run
from IPython.display import Image, display

from .. import Module

def get_script(n, modules, indices):
    script = ''

    consec_indices = list()
    control_indices = list()
    nop_indices = list()

    # Declare of boxes 
    for i in range(len(modules)):
        consec_index = list()
        if modules[i].controlled:
            for j in modules[i].reg_indices[0]:
                consec_index.append(indices[i][j])
        else:
            for j in indices[i]:
                consec_index.append(j)

        consec_index = list(range(min(consec_index), max(consec_index)+1))
        
        control_index = list()
        if modules[i].controlled:
            for j in modules[i].control_bits:
                if indices[i][j] not in consec_index:
                    control_index.append(indices[i][j])

        nop_index = list()
        ports = consec_index + control_index
        for j in list(range(min(ports), max(ports)+1)):
            if j not in ports:
                nop_index.append(j)

        nop_indices.append(nop_index)

        if modules[i].controlled:
            if len(consec_index) == 1:
                script += f"\tdef\tB{i},{len(control_index)},'{modules[i].sub_modules[0].name}'\n"
            else:
                script += f"\tdefbox\tB{i},{len(consec_index)+len(control_index)},{len(control_index)},'{modules[i].sub_modules[0].name}'\n"
        else:
            if len(consec_index) == 1:
                script += f"\tdef\tB{i},0,'{modules[i].name}'\n"
            else:
                script += f"\tdefbox\tB{i},{len(consec_index)},0,'{modules[i].name}'\n"

        consec_indices.append(consec_index)
        control_indices.append(control_index)

    # Declare of qubits
    for i in range(n):
        script += f'\tqubit\tq{i}\n';

    for i in range(len(modules)):
        script += f'\tB{i}\t'
        for j in control_indices[i]:
            script += f'q{j},'
        for j in consec_indices[i]:
            script += f'q{j},'
        script = script[:-1]
        script += '\n'
        if len(nop_indices[i]):
            for j in nop_indices[i]:
                script += f'\tnop\tq{j}\n'

    return script

def draw(module, option=''):
    if module.controlled:
        temp_module = Module(module.name, module.n, [module[list(range(module.n))]])
        draw(temp_module, option)
        return
    
    if option == 'decomposed':
        modules, indices = module.typ_decompose()
        script = get_script(module.n, modules, indices)
    else:
        script = get_script(module.n, module.sub_modules, module.reg_indices)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    qasm_script_path = current_dir + f'/{module.name}.qasm'
    qasm_script = open(qasm_script_path, 'w')
    qasm_script.write(script)
    qasm_script.close()

    run(current_dir + '/qasm2png ' + qasm_script_path, shell=True)

    display(Image(current_dir + f'/{module.name}.png'))
