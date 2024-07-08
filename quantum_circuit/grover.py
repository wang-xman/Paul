#!/usr/bin/env python3.6
#-*- coding:utf-8 -*-
"""
MODULE

quantum_circuit.grover.py

PATH

[app_root]/quantum_circuit/grover.py

INTRO

Grover search circuit.

CONTENT

TODO Need more circuits to find out:

[1] What are the common properties of all circuits?
Circuit is essentially a group of quantum flows merged
into one quantum flow.

[-2-] Oracle shall be provided by user. What is the interface?

[3] Should measurement be part of the circuit? Guess yes.

[4] Introduce errors.

LOG

Updated on 02 October 2020 | Created on 27 November 2020
"""
from math import ceil, pi, sqrt
from math import pow as power
from quantum_flow.quantum_flow import QuantumFlow
from quantum_flow.makers.reflection import reflection_flow_about_zeros
from quantum_flow.makers.walsh_hadamard import hadamard_flow_on_register


def initialise_flow(computer=None, ancilla=None):
    """ Initialisation flow

    Initialisation flow prepares computational register
    and ancilla register.

    TODO Check if computer register is in |00...0> and
    ancilla in |1>.
    """
    computer_init_flow = hadamard_flow_on_register(computer)
    ancilla_init_flow = hadamard_flow_on_register(ancilla)
    init_flow = computer_init_flow.merge(ancilla_init_flow)
    return init_flow


def reflection_flow(computer=None):
    """ Reflection flow """
    hadamard_flow = hadamard_flow_on_register(computer)
    reflec_flow = reflection_flow_about_zeros(computer)
    return hadamard_flow.merge(reflec_flow).merge(hadamard_flow)


def grover_G_flow(computer=None, oracle_operation=None):
    """ Grover operator flow """
    oracle_flow = QuantumFlow(operation=oracle_operation)
    reflec_flow = reflection_flow(computer=computer)
    return oracle_flow.merge(reflec_flow)


def number_of_iterations(noq=None):
    """ Number of iterations (noi) """
    noi = ceil(0.25 * pi * sqrt(power(2, noq)))
    return noi


def grover_search(computer=None, ancilla=None, oracle_operation=None):
    """ Main function : Grover search flow

    TODO

    [1] Must validate user-provided registers.

    [2] Must validate oracle operation.
    """
    noi = number_of_iterations(computer.noq)
    # init flow
    #init_flow = initialise_flow(computer=computer, ancilla=ancilla)
    # initialise total flow to grover_G
    #total_flow = grover_G_flow(computer=computer,
    #                       oracle_operation=oracle_operation)
    total_flow = initialise_flow(computer=computer, ancilla=ancilla)
    grover_g = grover_G_flow(computer=computer,
                             oracle_operation=oracle_operation)
    # merge iterations
    # TODO What happens? Why do I need only noi - 1 iterations?
    for _ in range(1, noi):
        total_flow = total_flow.merge(grover_g)
    return total_flow
