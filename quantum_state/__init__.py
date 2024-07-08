"""
PACKAGE

Quantum state

TODO

[1] Superposition. String repr

[2] Braket. How to link bra to quantum state conjugate.

PATH

[app_root]/quantum_state/

CONTENT

LOG

Updated on 25 September 2021 | Created on 20 June 2020
"""
from .null_state import NULL_STATE, NullState
from .quantum_state import QuantumState
from .superposition import QuantumSuperposition
from .braket import Bra, Ket
from .algebra import state_scale, state_add, state_sub, \
    state_inner, state_outer, state_kronecker, state_tensor
