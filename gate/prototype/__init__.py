"""
SUBPACK

Quantum gate prototype subpack.

PATH

[app_root]/gate/prototype/

INTRO

Gate prototype class implements the most basic
properties of a gate, including generating a
gate matrix.

CONTENT

`GatePrototype` - Generic gate prototype

`SingleQubitGatePrototype` - Gate prototype intended for
only single qubit gate

LOG

Updated on 02 October 2021 | Created on 22 September 2021
"""
from .base import GatePrototype, SingleQubitGatePrototype
