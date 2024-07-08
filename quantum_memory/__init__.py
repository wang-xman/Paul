#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
PACKAGE

Quantum memory

TODO This package is not really properly tested.

PATH

[app_root]/quantum_memory/

INTRO

Quantum memory consists of a textured layout of
quantum registers.

NOTE In the current version, the texture is a plain list.

CONTENT

LOG

Updated on 28 September 2021 | Created on 18 July 2021
"""
from .base_memory import BaseMemory
from .qubit_memory import QubitMemory
from .errors import QubitMemoryError
