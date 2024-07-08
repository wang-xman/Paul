#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.controlled.py

PATH

[app_root]/gate/enlarge_matrix/controlled.py

INTRO

Specialised matrix enlarge functions for construction
of controlled operator matrix.

CONTENT

`multiple_controlled_single_qubit_operator_matrix()` :
generic function to construct a multiple-controlled
operator matrix for a single-qubit gate

`single_controlled_single_qubit_operator_matrix()` :
construct a single-qubit controlled operator matrix for
a single-qubit operator gate; a special case to the more
generic multiple-controlled single-qubit operator


`single_controlled_multiple_qubit_operator_matrix ()` :
construct a single-qubit controlled multiple-qubit operator
matrix

`controlled_multiple_qubit_operator_matrix()`: construct
a controlled operator matrix for a mutiple-bit gate

LOG

Updated on 30 September 2021 | Created on 09 September 2021
"""
from .errors import GateMatrixEnlargeError
from .controlled_kernel import kernel
from .controlled_target_range import controlled_target_range
from .controlled_target_tuple import controlled_target_tuple

_MODULE_LOCATION_ = 'gate.enlarge_matrix.controlled'


def multiple_controlled_single_qubit(number_of_qubits=None, target_index=None,
                                     control_list=None, original_matrix=None):
    """ MCSQ - Multiple control bits and a single qubit operator

    A special case to generic: Only one target index.

    Multiple control bits on a single-qubit operator.
    As a generic resize function, it shall be able to
    handle the situation of just one control bit,
    see the following function.

    Consider a double-qubit controlled U operator.
    Assume the first two bits are used as control.
    With projection operator, this controlled operation
    consists of, the application part that involves U,
        `|1><1| x |1><1| x U`
    and, most importantly, other possibilities of the
    control bits, namely
        `|0><0| x |0><0| x I + |0><0| x |1><1| x I + |1><1| x |0><0| x I`,
    which simply means that, when the control bits are
    in these states, operator U is not applied to the
    target bit. Here `I` is a 2-by-2 identity matrix and
    symbol `x` is Kronecker product; `|0><0|` is the 2-by-2
    projection operator to 0 state and `|1><1|` is the
    projection to '1' state.

    Generalisation to a state of more bits is done by
    inserting identity matrix `I` to the bits that are
    not affected by this operation.

    Control index is therefore no longer one integer but
    a list of tuples, such as [(1,'0'),(2,'1'),(5,'1')],
    namely a control list to associate the control bit
    (index) with its condition (either '0' or '1').
    In the list, the first element of each tuple refers
    to the index of the control bit; the second element
    is a char that indicates if the control is conditional
    on state |0> or |1>. In this example, the control
    string is '011'.

    User provided control list will be validated and sorted
    in an ascending order in index. For example, control
    index [(2,'1'),(5,'1'),(1,'0')] after sorting shall
    become [(1,'0'),(2,'1'),(5,'1')].

    [Special case] Single-controlled operator is a special
    case which takes only one control bit. Consider a
    single-qubit matrix `U`, a 2-by-2 matrix as
    `original_matrix`, and the input state is an n-qubit
    state (and hence a dimension 2^n x 2^n). A formula for
    single-controlled operator is
        `I x...x I x |0><0| x I x...x I x...x I`
        `+ I x...x I x |1><1| x I x...x U x...x I`.
    The formula is composed of only two parts that are joined
    by a plus sign. This is due to the fact that there are
    only 2 possible states for a single control bit, '0' and '1'.

    ARGUMENTS:

    `number_of_qubits` (`int`) : total number of qubits of
    the multiple-qubit state to which the operator is applied

    `target_index` (`int`) : an integer that represents the
    index of the target bit in the scientific indexing scheme
    starting from 0

    `control_list` (`list`) : a list of tuples to associate the
    index of control bit with its condition (either '0' or '1');
    for example
        `[(1,'0'),(2,'1'),(5,'1')]`
    is a list specifying that qubits 1,2 and 5 are used as
    control bits, and their respective condition are '0',
    '1' and '1', giving to a control string '011'; control
    index must NOT overlap with `target_index`

    `original_matrix` (`SquareMatirx`) : the original single
    qubit matrix to be resized
    """
    total_matrix = None
    try:
        total_matrix = kernel(
            number_of_qubits=number_of_qubits,
            control_list=control_list,
            target_range=[target_index,target_index],
            original_matrix=original_matrix)
    except Exception as err:
        raise err
    return total_matrix


def single_controlled_single_qubit(number_of_qubits=None, target_index=None,
        control_index=None, control_state='1', original_matrix=None):
    """ SCSQ - Single-Controlled Single-Qubit operator matrix

    A special case to the generic. Only one control bit
    and hence the control index is just one integer.
    Conditional state for control bit is default to '1'.

    ARGUMENTS

    `number_of_qubits` (`int`) : total number of qubits in
    the target multi-qubit state

    `target_index` (`int`) : index of the target bit in the
    scientific indexing scheme starting from 0; it must be
    validated before resizing

    `control_index` (`int`) : index of the control bit in the
    scientific indexing scheme starting from 0; it must be
    validated before resizing; its value must NOT be same as
    `target_index`

    `control_state` (`str`) : state of the control bit, can
    be wither '0' or '1'; default is set to '1'

    `original_matrix` (`SquareMatirx`) : the original single
    qubit matrix to be resized

    RETURN

    `operator_matrix` (`SquareMatrix`) : newly constructed
    operator matrix
    """
    total_matrix = None
    try:
        total_matrix = kernel(number_of_qubits=number_of_qubits,
            control_list=[(control_index, control_state)],
            target_range=[target_index,target_index],
            original_matrix=original_matrix)
    except Exception as err:
        raise err
    return total_matrix


def single_controlled_multiple_qubit(number_of_qubits=None, target_range=None,
                                     control_index=None, original_matrix=None):
    """ SCMQ Single-Controlled Multiple-Qubit gate operator

    Construct a single-controlled multiple-qubit operator
    matrix.
    """
    total_matrix = None
    try:
        total_matrix = kernel(number_of_qubits=number_of_qubits,
            control_list=[(control_index, '1')],
            target_range=target_range,
            original_matrix=original_matrix)
    except Exception as err:
        raise err
    return total_matrix


# Most universal function
def universal_controlled(number_of_qubits=None, control_list=None,
        target_tuple=None, target_range=None, original_matrix=None):
    """ Generic controlled operator matrix

    Alias to multiple-controlled multiple-qubit operator matrix
    function.

    TODO Not tested.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.universal_controlled'
    # with target range
    if target_tuple is None and target_range is not None:
        return controlled_target_range(
            number_of_qubits=number_of_qubits,
            control_list=control_list,
            target_range=target_range,
            original_matrix=original_matrix)
    # with target index
    elif target_tuple is not None and target_range is None:
        return controlled_target_tuple(
            number_of_qubits=number_of_qubits,
            control_list=control_list,
            target_tuple=target_tuple,
            original_matrix=original_matrix)
    else:
        raise GateMatrixEnlargeError("Please provide either target index or " +\
                "target range. Not both.", location=_ERROR_LOCATION_)
