#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
PACKAGE

Quantum measurement

TODO

[1] Perhaps introduce decorators to regulate and
validate arguments in measurement functions.

PATH

[app_root]/measurement/

INTRO

Measurement package provides functions to perform
quantum measurement on a target represented by
either a quantum state or density matrix.

CONTENT

LOG

Updated on 27 September 2021 | Created on 08 April 2021
"""
from .partial_trace import partial_trace
from .projective import projective
