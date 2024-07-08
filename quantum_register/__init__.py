#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
PACKAGE

Quantum registers

PATH

[app_root]/quantum_register/

CONTENT

`QuantumRegister` - Quantum register object is a container
class that stores a generic quantum state as its internal state

`QubitRegister` - As a subclass to `QuantumRegister`, qubit
register stores a qubit state, i.e. an instance of `QubitState`,
as its internal state
"""
from .registers import QuantumRegister, QuantumAncillaRegister, QubitRegister, \
    ComputationalRegister, QubitAncillaRegister
