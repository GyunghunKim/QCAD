"""
Module nomm for class Nomm (No optimized matrix model)
Author: Gyunghun Kim
Date:   2018.09.01
"""

from . import MatrixModel


class Nomm(MatrixModel):
    """
    Class Nomm
    """
    def __init__(self, quantum_circuit):
        self.runable = True

