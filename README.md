# QCAD

Quantum Circuit Simulating Tool

## Installation

1. Clone this repository to your computer.
~~~
git clone https://github.com/GyunghunKim/QCAD.git
~~~
2. Compile it with cmake.
~~~
cmake .
make
~~~

## Dependency

1. camke and make (For compilation of C++ backend)
2. python2 (For drawing circuits)
3. python3 (For everything else)
4. numpy
5. latex with xypic (For drawing circuits)
6. netpbm (For drawing circuits)
7. csh (For drawing circuits)
- We are planning to eleminate the dependencies to python2 and csh.

## Extras

- Every circuit diagrams would be automatically saved in `./CircuitDrawer/`.
- The package qasm2circ of I. Chuang was deployed to draw quantum circuits.
- Link of the package qasm2circ: https://www.media.mit.edu/quanta/qasm2circ/

## Plans (2020. 06. 25.)

- Modules for performance test
- Parallel acceleration support including multicore cpus or gpus with new backends
