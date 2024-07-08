"""
SUBPACK

Specialised quantum flow makers

PATH

[app_root]/quantum_flow/makers/


"""
from .walsh_hadamard import WalshHadamardFlowError, hadamard_flow, \
    hadamard_flow_on_memory, hadamard_flow_on_register
from .swap import SwapFlowError, swap_flow, swap_flow_on_memory, \
    overall_swap_flow_on_register
from .fourier import FourierFlowError, quantum_fourier_flow_on_register, \
    inverse_quantum_fourier_flow_on_register
from .reflection import ReflectionFlowError, reflection_flow_about_zeros
