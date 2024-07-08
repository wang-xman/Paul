"""
MODULE

quantum_instruction.measurement.validators.py

PATH

[app_root]/quantum_instruction/measurement/validators.py

INTRO

Dedicated validators for measurement instruction subpack.

LOG

Updated on 01 October 2021 | Created on 13 August 2021
"""
from qubit import QubitState

from quantum_instruction.base import InstructionBaseValidator
from .errors import MeasurementInstructionDictValidationError

_MODULE_LOCATION_ = 'quantum_instruction.measurement.validators'


class MeasurementInstructionDictValidator(InstructionBaseValidator):
    """ Measurement instruction dictionary validator

    Measurement instruction dictionary has one required
    'register' key and one optional 'state' key.

    If 'state' is None or absent, the measurement is
    performed on all basis states of that register;
    if a qubit state is given, measurement is then
    performed on the given qubit state.
    """
    error_class = MeasurementInstructionDictValidationError
    error_location = _MODULE_LOCATION_ +\
            '.MeasurementInstructionDictValidator'
    accepted_keys = ['register', 'state']

    def __init__(self, instruc_dict=None):
        super().__init__()
        self._validated_dict = {}
        self.validate(instruc_dict)

    def validate(self, instruc_dict):
        """ Main method """
        if 'register' not in instruc_dict.keys():
            self.report_errors("Measurement operation " +\
                    "requires reference to a register.")
        elif not isinstance(instruc_dict['register'], str):
            self.report_errors("Register to be measured " +\
                    "must be referenced by its label as a string.")
        else:
            self._validated_dict['register'] = instruc_dict['register']

        if self.is_valid:
            if 'state' in instruc_dict.keys():
                if not isinstance(instruc_dict['state'], QubitState):
                    self.report_errors("State used in " +\
                            "projective measurement is not a qubit.")
                else:
                    self._validated_dict['state'] = instruc_dict['state']

    def validated_data(self):
        return self._validated_dict
