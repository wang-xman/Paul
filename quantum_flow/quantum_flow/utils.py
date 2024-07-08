from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory, QubitRegisterMetadata

from .errors import BaseQuantumFlowError

_MODULE_LOCATION_ = 'quantum_flow.quantum_flow.utils'


# TODO Not independently tested.
# FIXME What if only register label is provided?
# Validation functions
def validate_register_for_flow(register, caller_location=None):
    """ Validate register for flow makers

    Raises error if register is not compatible for making
    quantum flows.

    ARGUMENTS

    `register` (`QubitRegister` or `QubitRegsiterMetadata`) :
    a qubit register or qubit-regsiter metadata

    `caller_location` (`str`) : a string variable specifying
    a caller function's location
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.validate_register_for_flow'
    # set error location
    if caller_location is not None and isinstance(caller_location, str):
        error_location = caller_location
    else:
        error_location = _ERROR_LOCATION_
    if not isinstance(register, (QubitRegisterMetadata, QubitRegister)):
        raise BaseQuantumFlowError("Quantum operation flow " +\
                "for register requires either a register " +\
                "or metadata of a register.", location=error_location)


def validate_memory_for_flow(memory, caller_location=None):
    """ Validate memory for flow makers

    Raises error if memory is not compatible for making
    quantum flows.

    ARGUMENTS

    `memory` (`QubitMemory`) : an active qubit memory

    `caller_location` (`str`) : a string variable specifying
    a caller function's location
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.validate_memory_for_flow'
    # set error location
    if caller_location is not None and isinstance(caller_location, str):
        error_location = caller_location
    else:
        error_location = _ERROR_LOCATION_
    if not isinstance(memory, QubitMemory):
        raise BaseQuantumFlowError("Quantum operation flow" +\
                "for memory requires a qubit memory.",
                location=error_location)


def validate_local_index_on_register(local_index=None, register=None,
                                     caller_location=None):
    """ Validate a local index against register (metadata)

    Raises error if the given local index is not compatible with
    the given register.

    ARGUMENTS

    `local_index_a` (`int`) : local index of the bit to be swapped

    `local_index_b` (`int`) : local index of the bit to be swapped

    `register` (`QubitRegister` or `QubitRegsiterMetadata`) :
    a qubit register or qubit-regsiter metadata
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ +\
            '.validate_local_index_on_register'
    # set error location
    if caller_location is not None and isinstance(caller_location, str):
        error_location = caller_location
    else:
        error_location = _ERROR_LOCATION_
    if not local_index in range(0, register.noq):
        raise BaseQuantumFlowError("Index 'local_index' " +\
                "is outside the range of " +\
                "register '{}'.".format(register.label),
                location=error_location)
