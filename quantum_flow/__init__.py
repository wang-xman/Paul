#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
PACKAGE

Quantum Flow

PATH

[app_root]/quantum_flow/

TODO

[1] For flow makers, introduce decorators to systematically
validate index, register and memory.

INTRO

Quantum flow executes a sequence of quantum operations
on a quantum memory.

CONTENT

LOG

Updated on 02 October 2021 | Created on 18 July 2021
"""
from .quantum_flow.quantum_flow import QuantumFlow, QuantumFlowError
from .makers import WalshHadamardFlowError, hadamard_flow, \
    hadamard_flow_on_memory, hadamard_flow_on_register, \
    SwapFlowError, swap_flow, swap_flow_on_memory, \
    overall_swap_flow_on_register, \
    FourierFlowError, quantum_fourier_flow_on_register, \
    inverse_quantum_fourier_flow_on_register, \
    ReflectionFlowError, reflection_flow_about_zeros
