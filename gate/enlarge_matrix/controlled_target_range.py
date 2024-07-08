#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.controlled_target_range.py

PATH

[app_root]/gate/enlarge_matrix/controlled_target_range.py

INTRO


CONTENT

`controlled_target_range()` - Alias to the
function above

LOG

Updated on 17 September 2021 | Created on 17 September 2021
"""
from .controlled_kernel import kernel


def controlled_target_range(number_of_qubits=None, target_range=None,
                            control_list=None, original_matrix=None):
    """ Target range is provided. """
    return kernel(
            number_of_qubits=number_of_qubits,
            control_list=control_list,
            target_range=target_range,
            original_matrix=original_matrix)
