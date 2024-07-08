#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
PACKAGE

Quantum gate

PATH

[app_root]/gate/

INTRO

Quantum gate is one of the most important components
in a quantum circuit. Gate is designed for application
on qubits.

CONTENT

`single_qubit_gates` (`dict`) - A dictionary that
stores single qubit gates. Keys to this dictionary
are the aliases of the corresponding gates.

LOG

Updated on 30 September 2021 | Created on 29 June 2020
"""
from . import single_qubit
single_qubit.registration()

single_qubit_gates = single_qubit.gatelib


def has_gate(alias):
    ret = False
    if alias in single_qubit_gates.keys():
        ret = True
    return ret
