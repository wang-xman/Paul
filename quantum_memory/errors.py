#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.errors.py

PATH

[app_root]/quantum_memory/errors.py

INTRO

Dedicated errors

CONTENT

LOG

Updated on 01 October 2021 | Created on 18 July 2021
"""
from .base import QuantumMemoryBaseError, QuantumMemoryBaseValidationError


class QubitMemoryRegisterValidationError(QuantumMemoryBaseValidationError):
    """
    ENTRY

    `validators.QubitMemoryRegisterValidator`
    """
    header = 'Qubit_Memory_Register_Validation_Error'


class OperationLauncherValidationError(QuantumMemoryBaseValidationError):
    """
    ENTRY

    `validators.OperationLauncherValidator`
    """
    header = 'Operation_Launcher_Validation_Error'


class QuantumMemoryError(QuantumMemoryBaseError):
    """ Generic error class
    ENTRY

    `base_memory.BaseMemory`
    """
    header = 'Quantum_Memory_Error'


class RegisterMetadataError(QuantumMemoryError):
    """ Error raised by register metadata
    ENTRY

    `metadata.BaseRegisterMetadata`
    """
    header = 'Register_Metadata_Error'


class ManagerError(QuantumMemoryError):
    """ Error raised by managers """
    header = 'Manager_Error'

class RegisterMetadataManagerError(ManagerError):
    """ Error raised by register manager

    ENTRY

    `managers.RegisterMetadataManager`
    """
    header = 'Register_Metadata_Manager_Error'

class IndexManagerError(ManagerError):
    """ Error raise by index manager

    ENTRY

    `managers.IndexManager`
    """
    header = 'Index_Manager'


class QubitRegisterMetadataError(RegisterMetadataError):
    """ Error raised by qubit register metadata

    ENTRY

    `qubit_memory.QubitRegisterMetadata`
    """

class QubitMemoryError(QuantumMemoryError):
    """ Error raised by qubit memory

    ENTRY
    `qubit_memory.QubitMemory`
    """
