"""
Module backend for class Backend
Author: Gyunghun Kim
Date:   2018.09.01

Every backend simulator models must inherit from class Backend.
"""

class Backend(object):
    """
    Class Backend
    """
    def __init__(self, quantum_circuit):
        self.runable = False
        self.quantum_circuit = quantum_circuit
