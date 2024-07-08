"""
MODULE

quantum_operation.gate.validators.py

PATH

[app_root]/quantum_operation/gate/validators.py

INTRO

Dedicate validators for gate opertaion

LOG

Updated on 02 October 2021 | Created on 12 July 2021
"""
from quantum_operation.base import OperationBaseValidator
from .errors import GateOperationValidationError

_MODULE_LOCATION_ = 'quantum_operation.gate.validators'


class GateOperationValidator(OperationBaseValidator):
    """ Validate operation against a memory

    Mainly checks the compatibility of an operation
    instruction against the provided memory.

    Main task of this validator is to verify that all
    local indices are in the range of their respective
    register.
    """
    error_class = GateOperationValidationError
    error_location = _MODULE_LOCATION_ + '.GateOperationValidator'

    def __init__(self, instruction=None, memory=None):
        super().__init__()
        self.validate(instruc=instruction, memory=memory)

    def validate_target(self, target=None, memory=None):
        """ Validate target dictionary against memory """
        if not memory.has_register_label(target['register']):
            self.report_errors("Target register " +\
                    "'{}' does not exist ".format(target['register']) +\
                    "in memory '{}'.".format(memory.label),
                    location=self.error_location+".validate_target")
        elif target['local_index'] \
                not in memory.get_local_index_range_by_label(target['register']):
            self.report_errors("Target index " +\
                    "{} is outside the ".format(target['local_index']) +\
                    "range of register '{}' ".format(target['register']) +\
                    "in memory '{}'.".format(memory.label),
                    location=self.error_location+".validate_target")
        else:
            pass

    def validate_control(self, control=None, memory=None):
        for i, el in enumerate(control['list']):
            if not memory.has_register_label(el['register']):
                self.report_errors("Register "+\
                    "'{}' ".format(el['register']) +\
                    "indexed by {} in control list ".format(i) +\
                    "cannot be found in memory '{}'.".format(memory.label),
                    location=self.error_location+".validate_control")
            elif el['local_index'] \
                    not in memory.get_local_index_range_by_label(el['register']):
                self.report_errors("Control index " +\
                        "{} is outside the local ".format(el['local_index']) +\
                        "range of register '{}' ".format(el['register']) +\
                        "in memory '{}'.".format(memory.label),
                        location=self.error_location+".validate_control")
            else:
                pass

    def validate(self, instruc=None, memory=None):
        """ Main validation method """
        self.validate_target(target=instruc.target_dict, memory=memory)
        if instruc.has_control:
            self.validate_control(control=instruc.control_dict, memory=memory)
