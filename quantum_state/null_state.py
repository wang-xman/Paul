#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.null_state.py

PATH

[app_root]/quantum_state/null_state.py

INTRO

Null state object. Null state represents the subtraction
of two quantum states. This definition is conceptually
different from a state vector that is filled with only
zeros.

LOG

Updated on 25 September 2021 | Created on 20 June 2020
"""
from .base import AbstractQuantumState


class NullState(AbstractQuantumState):
    """ Null state

    Null state is an abstract quantum state and it
    represents the substraction of two identical states.

    Null state is a singleton.

    Null state must be distinguished in cencept from a state
    that is represented by a vector with only 0.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass


NULL_STATE = NullState()
""" Null state singleton """
