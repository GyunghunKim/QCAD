"""
Module execute for function execute
Author: Gyunghun Kim
Date:   2018.09.01

Function execute connects between front-end and back-end.
"""

from . import Backend


def execute(quantum_circuit, backend):
    """
    :param quantum_circuit: 게이트와 레지스터가 정의된 QuantumCircuit 객체
    :param backend: backend의 타입을 string 형태로 명시
    :return: Result 객체를 리턴
    """

    # No Optimized Matrix Model
    if backend is "NOMM":
        Backend.Nomm(quantum_circuit)

    # Cuda Optimized Matrix Model
    if backend is "COMM":
        Backend.Comm(quantum_circuit)
