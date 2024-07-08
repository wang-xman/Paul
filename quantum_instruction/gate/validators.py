"""
MODULE

quantum_instruction.gate.validators.py

PATH

[app_root]/quantum_instruction/gate/validators.py

INTRO

Dedicated validators for gate instruction subpack.

LOG

Updated on 01 October 2021 | Created on 12 August 2021
"""
from warnings import warn
from gate.decorator import as_gate
from gate import has_gate
from gate import single_qubit_gates as singles

from quantum_instruction.base import InstructionBaseValidator
from .errors import GateInstructionDictValidationError

_MODULE_LOCATION_ = 'quantum_instruction.gate.validators'


class GateSubdictValidator(InstructionBaseValidator):
    """ Gate subdict valdiator

    Validate gate subdict in an instruction for gate operation.

    A gate subdict must contain either a key 'instance' to
    identify user-defined gate, or a key `alias` to identify
    and request gate from existing gate repertoire.

    Should the gate prototype contain a `parameters` descriptor,
    the gate subdict must also have a key `parameters` and it
    can be empty, indicating default (parameters) values are used.

    In general, gate subdict is
        {
            'instance': a user-defined gate instance,
            'alias': a `str`; required key to identify gate,
            'paramters': a `dict`; optional, depending on gate
                          prototype
        }
    For example,
        {
            'alias': `PhaseRotation`,
            'parameters': {
                'n': 0,
                'm': 1
            }
        }
    is a dictionary that describes a phase rotation gate operator
    from gate repertoire with parameters `n` and `m` set to given
    values.

    Another example,
        {
            'instance': [A gate instance]
            'parameters': {
                'x': 0,
                'y': 1
            }
        }
    is a dictionary that describes a user-defined gate operator
    with parameters. This user-defined gate operator is not
    acquired from default gate repertoire. In this case, key
    'alias' is optional and its value, should be provided, is
    checked against the instance's alias.
    """
    error_class = GateInstructionDictValidationError
    error_location = _MODULE_LOCATION_ + '.GateSubdictValidator'

    def __init__(self, gate_dict=None):
        super().__init__()
        self.validate(data=gate_dict)

    def validate_user_defined_gate(self, data=None):
        """ Instruction Gate Subdict Validator :: User-defined gate """
        if not isinstance(data['instance'], as_gate):
            self.report_errors("User-defined gate " +\
                    "must be an instance of 'as_gate' decorator.")
        else:
            if 'alias' in data.keys():
                if data['alias'] != data['instance'].alias:
                    self.report_errors("User-defined gate " +\
                            "{} has ".format(data['instance'].alias) +\
                            "a different alias '{}'.".format(data['alias']))
            if not data['instance'].gate_prototype.parameters == {}:
                if 'parameters' not in data.keys() \
                        or not isinstance(data['parameters'], dict):
                    self.report_errors("User-defined gate " +\
                            "{} used in ".format(data['instance'].alias) +\
                            "operation must have a parameters " +\
                            "dictionary which can be empty.")

    def validate(self, data=None):
        """ Instruction Gate Subdict Validator :: Main method

        Should key 'instance' exists, key 'alias' is optional and
        merely provides the alias of the user-defined gate instance.
        """
        if 'instance' in data.keys() and data['instance'] is not None:
            # user-defined gate instance
            self.validate_user_defined_gate(data=data)
        else:
            if 'alias' not in data.keys():
                self.report_errors("Gate used in an operation " +\
                        "must be identified by its alias in gate repertoire.")
            elif not isinstance(data['alias'], str):
                self.report_errors("Alias used to identify a " +\
                        "quantum gate is not a string.")
            else:
                # gate not found
                if not has_gate(data['alias']):
                    self.report_errors("Gate referenced by alias " +\
                            "'{}' ".format(data['alias']) +\
                            "cannot be found in gate repertoire.")
                # gate found
                else:
                    # gate prototype has non-empty parameters
                    if not singles[data['alias']].gate_prototype.parameters == {}:
                        if 'parameters' not in data.keys() \
                                or not isinstance(data['parameters'], dict):
                            self.report_errors("Gate " +\
                                    "{} used in ".format(data['alias']) +\
                                    "operation must have a parameters " +\
                                    "dictionary which can be empty.")


class TargetSubdictValidator(InstructionBaseValidator):
    """ Target subdict validator

    Validate target sub-dictionary which has two keys.

    Key `register` is a string refering to a register's label.
    Key `local_index` is the local index of the target bit.

    In summary, a target subdict is
        {
            'register': a `str` value, reference to register
            'local_index': a `int`, local index of target bit
        }

    NOTE Current version only allows single-qubit target.
    """
    error_class = GateInstructionDictValidationError
    error_location = _MODULE_LOCATION_ + '.TargetSubdictValidator'

    def __init__(self, target_dict=None):
        super().__init__()
        self.validate(data=target_dict)

    def validate(self, data=None):
        """ Operation Target Validator :: Main method """
        if 'register' not in data.keys():
            self.report_errors("Target in an operation " +\
                    "is missing a reference to register's label.")
        elif 'local_index' not in data.keys():
            self.report_errors("Target in an operation " +\
                    "is missing a local index referencing to it.")
        else:
            if not isinstance(data['register'], str):
                self.report_errors("Label to reference a " +\
                        "register is not a string.")
            elif not isinstance(data['local_index'], int):
                self.report_errors("Local index to reference " +\
                        "the target bit in register is not an integer.")


class ControlSubdictElementValidator(InstructionBaseValidator):
    """ Control subdict element validator

    Control element details a qubit used for control operation.
    A control element is described by a dictionary consisting
    of three keys,
        {
            'register': a `str` variable referencing register label,
            'local_index': an `int` referencing local index of the qubit,
            'state': single char either '0' or '1'
        }
    """
    error_class = GateInstructionDictValidationError
    error_location = _MODULE_LOCATION_ + '.ControlSubdictElementValidator'

    accepted_control_state = ['0', '1']
    accepted_control_keys = ['register', 'local_index', 'state']

    def __init__(self, element=None):
        super().__init__()
        self.validate(data=element)

    def validate(self, data=None):
        if 'register' not in data.keys():
            self.report_errors("Element in control " +\
                    "list is missing a reference to register's label.")
        elif 'local_index' not in data.keys():
            self.report_errors("Element in control " +\
                    "list is missing the required local index.")
        elif 'state' not in data.keys():
            self.report_errors("Element in control " +\
                    "list is missing the state for control.")
        else:
            if not isinstance(data['register'], str):
                self.report_errors("Label to reference a " +\
                        "register for control element is not a string.")
            elif not isinstance(data['local_index'], int):
                self.report_errors("Local index of a control " +\
                        "element is not an integer.")
            elif data['state'] not in self.accepted_control_state:
                self.report_errors("State of a control " +\
                        "element is neither '0' nor '1'. " +\
                        "Invalid control state.")
            else:
                for key, _ in data.items():
                    if key not in self.accepted_control_keys:
                        warn("Control element consists of a unknown " +\
                                "key '{}'. ".format(key) +\
                                "It is ignored in the operation.")


class ControlSubdictValidator(InstructionBaseValidator):
    """ Control sub-dictionary validator

    Control sub-dictionary consists of one key `list` to
    reference the list of control elements. Each control
    element is described by a dictionary of three keys
    (see control element validator).

    Validation is performed on the outfit of the list as
    well as at element level via `ControlSubdictElementValidator`.

    In summary, the control dictionary is
        {
            'list': [
                {
                    'register': 'reg1',
                    'local_index': 0,
                    'state': '1'

                },
                {
                    'register': 'reg1',
                    'local_index': 1,
                    'state': '1'

                },
                ...
            ]
        }
    Identical control elements (same index in the same register) are
    ruled out. Each control element is checked against the target bit
    to rule out control-target clash.
    """
    error_class = GateInstructionDictValidationError
    error_location = _MODULE_LOCATION_ + '.ControlSubdictValidator'

    def __init__(self, control_dict=None, target_dict=None):
        super().__init__()
        self.validate(data=control_dict, target=target_dict)

    def _rule_out_double_entry(self, data=None):
        elist = data['list']
        for i in range(0, len(elist)):
            for j in range(i+1, len(elist)):
                if elist[i]['register'] == elist[j]['register'] \
                        and elist[i]['local_index'] == elist[j]['local_index']:
                    self.report_errors("In the control list, " +\
                        "items indexed {} and {} ".format(i,j) +\
                        "are the same qubit in the same register.")

    def validate(self, data=None, target=None):
        if 'list' not in data.keys():
            self.report_errors("Control in an operation " +\
                    "is missing a control list.")
        elif not isinstance(data['list'], list):
            self.report_errors("Control list required " +\
                    "to specify control bits is not a list.")
        else:
            for i, el in enumerate(data['list']):
                elvalidator = ControlSubdictElementValidator(element=el)
                if not elvalidator.is_valid:
                    # fetch the index of erratic element
                    errheader = "Element indexed {} on the list. ".format(i)
                    errmsg = errheader + elvalidator.get_errors()[0].message
                    self.report_errors(errmsg)
                else:
                    if el['register'] == target['register'] \
                            and el['local_index'] == target['local_index']:
                        self.report_errors("In the control list, " +\
                                "item with index {} ".format(i) +\
                                "clashes with the target bit of local "+\
                                "index {} ".format(target['local_index']) +\
                                "in register '{}'.".format(target['register']))
            # rule out double entry
            if self.is_valid and len(data['list']) > 1:
                self._rule_out_double_entry(data=data)


class GateInstructionDictValidator(InstructionBaseValidator):
    """ Gate instruction validator

    Validates integrity and consistency of an instruction
    dictionary.
    """
    error_class = GateInstructionDictValidationError
    accepted_keys = ['gate', 'target', 'control']
    error_location = _MODULE_LOCATION_ + '.GateOperationInstructionValidator'

    def __init__(self, instruc_dict=None):
        super().__init__()
        self.validate(data=instruc_dict)

    def validate_overall(self, instruc_dict=None):
        """ Overall validate

        Sub-dictionaries 'gate' and 'target' are required, and 'control'
        subdict is optional.
        """
        if not isinstance(instruc_dict, dict):
            self.report_errors("Instruction dictionary for " +\
                    "gate operation is not a valid dictionary.")
        elif 'gate' not in instruc_dict.keys():
            self.report_errors("Instruction dictionary for " +\
                    "gate operation is missing a 'gate' sub-dictionary.")
        elif 'target' not in instruc_dict.keys():
            self.report_errors("Instruction dictionary for " +\
                    "gate operation is missing a 'target' sub-dictionary.")
        else:
            pass

    def validate_gate(self, data=None):
        """ Validate gate sub-dictionary """
        validator = GateSubdictValidator(gate_dict=data)
        if not validator.is_valid:
            self.report_errors(validator.get_errors())

    def validate_target(self, data=None):
        """ Validate target sub-dictionary """
        validator = TargetSubdictValidator(target_dict=data)
        if not validator.is_valid:
            self.report_errors(validator.get_errors())

    def validate_control(self, data=None, target_dict=None):
        """ Validate control sub-dictionary

        Also checks if a control bit clashes with target.
        """
        validator = ControlSubdictValidator(control_dict=data,
                                            target_dict=target_dict)
        if not validator.is_valid:
            self.report_errors(validator.get_errors())

    def validate(self, data=None):
        """ Main validation method

        Control is validated only when there is a control dictionary.
        """
        self.validate_overall(instruc_dict=data)
        if self.is_valid:
            self.validate_gate(data=data['gate'])
            self.validate_target(data=data['target'])
            if 'control' in data.keys():
                self.validate_control(data=data['control'],
                                      target_dict=data['target'])
        # warning: unknown keys
        if self.is_valid:
            for key, _ in data.items():
                if key not in self.accepted_keys:
                    warn("Parameter named '{}' in operation ".format(key) +\
                            "dictionary is unknown. This parameter and " +\
                            "its value won't be used.")
