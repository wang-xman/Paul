"""
SUBPACK

Quantum state algebra

PATH

[app_root]/quantum_state/algebra

INTRO

Quantum state algebra functions (QSAF).

CONTENT

LOG

Updated on 29 September 2021 | Created on 20 June 2020
"""
from .errors import QuantumStateAlgebraFunctionError
from .functions import state_scale, state_add, state_sub, state_inner, \
    state_outer, state_kronecker, state_kron, state_tensor
