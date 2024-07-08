#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_instruction.gate.instructions.py

PATH

[app_root]/quantum_instruction/gate/instructions.py

INTRO

User-provided instruction dictionary for gate operation
has three subdicts to describe Gate, Target and Control.

- Gate. A dictionary describes a quantum gate operator.
Data in this dictionary is used to request and instantiate
a gate operator, either from existing gate repertoire or
user-defined gate instances.

- Target. Describes the reference to a qubit on a particular
register. Key `local_index` is used to identify the target
qubit on register. TODO How to extend to multiple target?

- Control. If exists, the intended operation is a controlled
one. It describes a list of control bits used in operation.
Each control bit is further described by a dictionary detailing
its location and state.

As an example, a typical gate operation dictionary may look
like the following
    {
        'gate': {
            'alias': 'PhaseRotation',
            'parameters': {
                'n': 0,
                'm': 1
            }
        },
        'target': {
            'register': `reg2`,
            'local_index': 0
        },
        'control': {
            'list': [
                {
                    'register': 'reg1',
                    'local_index': 0,
                    'state': '0'
                },
                {
                    'register': 'reg1',
                    'local_index': 1,
                    'state': '1'
                }
            ]
        }
    }
which requests a gate operator with alias 'PhaseRotation' from
existing gate repertoire.

User-defined gate may enter instruction dictionary via key
'instance' which has a gate instance as its value, for example,
    {
        'gate': {
            'instance': [A gate instance],
            'parameters': {
                'n': 0,
                'm': 1
            }
        },
        'target': {
            'register': `reg2`,
            'local_index': 0
        },
        'control': {
            'list': [
                {
                    'register': 'reg1',
                    'local_index': 0,
                    'state': '0'
                },
                {
                    'register': 'reg1',
                    'local_index': 1,
                    'state': '1'
                }
            ]
        }
    }

In the current version, one gate operation describes only one
single-qubit gate operator. The target is thus required to be
a single qubit, too. Multiple-qubit target is in principle
possible, but the known difficulty in physical realisation in
a near term quantum computer puts it off from the current version.

TODO

[-1-] Make instruction to accept usre-defined gate instance.

[2] Extend target to multiple-qubit state. This is a must
in algorithms such as phase estimation and amplitude
estimation. Change to be made in gate application.

LOG

Updated on 01 October 2021 | Created on 12 August 2021
"""
from .validators import GateInstructionDictValidator

__MODULE_LOCATION__ = 'quantum_instruction.gate.instructions'


class GateInstruction:
    """ Gate(-operation) instruction object

    Gate instruction converts a JSON-like instruction
    dictionary into an instruction object.

    Quantum instruction object is supposed to be embedded
    in an operation via composition.
    """
    def __init__(self, instruc_dict):
        validator = GateInstructionDictValidator(instruc_dict=instruc_dict)
        if validator.is_valid:
            self._internal_dict = instruc_dict
        else:
            validator.raise_last_error()

    @property
    def gate_dict(self):
        """ Gate Instruction :: Returns gate dictionary """
        return self._internal_dict.get('gate')

    @property
    def has_gate_instance(self):
        """ Gate Instruction :: Verifies if has gate instance

        Returns `True` if a gate instance exists and it means
        a user-defined gate operator has been provided.
        """
        ret = False
        if 'instance' in self._internal_dict.get('gate').keys():
            ret = True
        return ret

    @property
    def gate_instance(self):
        """ Gate Instruction :: Returns gate instance

        If gate instance is None, returns None.
        """
        ret = None
        if self.has_gate_instance:
            ret = self._internal_dict.get('gate').get('instance')
        return ret

    @property
    def gate_alias(self):
        """ Gate Instruction :: Returns gate alias """
        alias = None
        if self.has_gate_instance:
            alias = self._internal_dict.get('gate').get('instance').alias
        else:
            alias = self._internal_dict.get('gate').get('alias')
        return alias

    @property
    def target_dict(self):
        """ Gate Instruction :: Returns target dict """
        return self._internal_dict.get('target')

    @property
    def has_control(self):
        """ Gate Instruction :: Verify if a controlled one """
        ret = False
        if 'control' in self._internal_dict.keys():
            ret = True
        return ret

    @property
    def control_dict(self):
        """ Gate Instruction :: Returns control dict """
        ret = None
        if self.has_control:
            ret = self._internal_dict.get('control')
        return ret

    def get_control_list(self):
        """ Gate Instruction :: Returns control list

        In case no controls, returned list is an empty list.
        """
        ret = None
        if self.has_control:
            ret = self._internal_dict.get('control')['list']
        else:
            ret = []
        return ret
