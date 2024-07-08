#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.utils.py

PATH

[app_root]/bit/utils.py

INTRO

Utility functions that interconvert bitstring with integer,
fraction and standard basis.

Uitlity module is thus higher in the module hierarchy than
others, as bit wrapper objects are depedent on it.

LOG

Updated on 30 September 2021 | Created on 06 November 2020
"""
from linear_space.numpy_lib import np_intc, np_array

from linear_space.number import power_of_two, exponent_of_two, is_zero
from linear_space.vector import StandardBasisVector
from linear_space.algebra import scale, matrix_add

from .errors import BitUtilityFunctionError
from .validators import BitarrayValidator, BitlistValidator, BitstringValidator

_MODULE_LOCATION_ = 'bit.utils'


def is_index_valid_on_bitstring(bitstring, index):
    """ Verify if an index is valid """
    ret = False
    if index in range(0, len(bitstring), 1):
        ret = True
    return ret


def bitarray_to_integer(bitarray):
    """ Convert an array of bits into a decimal integer

    Conversion rule. First element in array is associated
    with the highest power in 2; last element is with
    the lowest power.

    For example, array([0,1,0]) is converted into 2 via
    binary function 0x2^2 + 1x2^1 + 0x2^0 = 2, where each
    element is the coefficient (not power).
    """
    ret = None
    integer = 0
    validator = BitarrayValidator(bitarray=bitarray)
    if validator.is_valid:
        validated_array = validator.validated_data()['bitarray']
        number_of_digits = len(validated_array)
        for i, digit in enumerate(validated_array):
            integer += digit * power_of_two(number_of_digits - 1 - i)
        ret = np_intc(integer)
    else:
        validator.raise_last_error()
    return ret


def bitstring_to_integer(bitstring):
    """ Convert a bitstring into a decimal integer.

    Bitstring is converted into a list of binaries then
    invoking `bitarray_to_integer` method.

    RETURN

    A decimal integer number
    """
    bitlist = [np_intc(digit) for digit in bitstring]
    return bitarray_to_integer(bitlist)


def integer_to_bitstring(integer=None, total_digits=None):
    """ Converts a decimal integer to a bitstring.

    To meet the required total number of digits, zeros are
    pre-appended to the string. For example, integer 1 is
    converted into 001 (3 digits) or 01 (2 digits).

    However, if the bitstring of the required integer is
    longer than the specific total digits, the total digits
    argument will be ignored.

    RETURN

    A bitstring
    """
    convert_string = "{0:0" + str(total_digits) + "b}"
    bitstring = convert_string.format(np_intc(integer))
    return bitstring


def bitstring_to_fraction(bitstring):
    """ Convert a bitstring into a decimal fraction

    Conversion rule. First element is associated with
    the lowest power of 1/2, i.e. (1/2)^1; the last element
    is thus associated with the highest power of 1/2.

    For example '0011' is often denoted as '0.0011' to
    highlight that it represents fraction. It is converted
    into a decimal fraction via
        `0*(1/2)^1 + 0*(1/2)^2 + 1*(1/2)^3 + 1*(1/2)^4`
    and the corresponding decimal number is 0.1875.

    RETURN

    A decimal fraction number
    """
    fraction = 0.0
    number_of_digits = len(bitstring)
    for idx in range(0, number_of_digits, 1):
        digit = int(bitstring[idx])
        fraction = fraction + digit * 1.0 / power_of_two(idx+1)
    return fraction


def bitstring_to_standard_basis(bitstring):
    """ Convert a bitstring into a standard basis vector

    Bitstring is converted into `StandardBasisVector`
    instance for qubits.

    RETURN

    A standard basis vector instance
    """
    number_of_qubits = len(bitstring)
    size = power_of_two(number_of_qubits)
    iloc = bitstring_to_integer(bitstring)
    return StandardBasisVector(iloc=iloc, size=size)


def integer_to_bitarray(integer=None, total_digits=None):
    """ Convert a decimal integer into an array of binaries.

    For example, integer 1 is converted into `array([0,0,1])`
    as a 3-digit binary code, or `array([0,1])` as a 2-digit
    binary code.
    """
    bitstring = integer_to_bitstring(
            integer=int(integer), total_digits=int(total_digits))
    bitlist = []
    for item in bitstring:
        bitlist.append(np_intc(item))
    return np_array(bitlist, dtype=np_intc)


def bitlist_to_vector(src_bitlist):
    """ Convert a bitlist to a vector

    Bitstring in the list is first converted into a standard
    basis vector; all standard basis vectors are then scaled
    with the corresponding amplitudes; finally, scaled vectors
    are then summed up.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_+'.bitlist_to_vector'

    validator = BitlistValidator(bitlist=src_bitlist)
    if validator.is_valid:
        vector = scale(src_bitlist[0][0],
                       bitstring_to_standard_basis(src_bitlist[0][1]))
        # if there is more than one component
        if len(src_bitlist) > 1:
            for i in range(1, len(src_bitlist), 1):
                vec = scale(src_bitlist[i][0],
                            bitstring_to_standard_basis(src_bitlist[i][1]))
                vector = matrix_add(vector, vec)
    else:
        raise BitUtilityFunctionError(str(validator.get_errors()),
                                      location=_ERROR_LOCATION_)
    return vector


def vector_to_bitlist(vector):
    """ Convert a column vector to a bitlist

    Returns a bitlist of tuples like [(0.5, '00'), (0.5, '11')].

    In each tuple, first element is the amplitude (a complex number),
    and the second is the bitstring representing the basis state.

    Zero amplitude removal. If the amplitude is smaller than 10e-16,
    the associated component will be neglected and removed.

    FIXME Not unittested.
    """
    bitlist = []
    # calculate number of qubits
    noq = exponent_of_two(vector.size)
    for i, amp in enumerate(vector.as_array()):
        # zero amplitude removal
        if not is_zero(amp[0]):
            # convert an integer to binary string
            bitstring = integer_to_bitstring(integer=i, total_digits=noq)
            bitlist.append((amp, bitstring,))
    return bitlist


# bitwise operations
def flip_bit(src_bitstring, index):
    """ Flip a selected bit in bitstring """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.flip_bit'
    new_string = ''
    validator = BitstringValidator(bitstring=src_bitstring)
    if validator.is_valid:
        if is_index_valid_on_bitstring(src_bitstring, index):
            for i, bit in enumerate(src_bitstring):
                if i == index:
                    if bit == '0':
                        new_string += '1'
                    else:
                        new_string += '0'
                else:
                    new_string += bit
        else:
            raise BitUtilityFunctionError('Bit index out of range.',
                                          location=_ERROR_LOCATION_)
    else:
        raise BitUtilityFunctionError(validator.get_errors(),
                                      location=_ERROR_LOCATION_)
    return new_string


def flip_all(src_bitstring):
    """ Flip all bits """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.flip_all'
    new_string = ''
    validator = BitstringValidator(bitstring=src_bitstring)
    if validator.is_valid:
        for bit in src_bitstring:
            if bit == '0':
                new_string += '1'
            else:
                new_string += '0'
    else:
        raise BitUtilityFunctionError(validator.get_errors(),
                                      location=_ERROR_LOCATION_)
    return new_string


def swap_bits(src_bitstring, index_one, index_two):
    """ Swap two bits """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.swap_bits'
    new_string = ''
    validator = BitstringValidator(bitstring=src_bitstring)
    if validator.is_valid:
        if is_index_valid_on_bitstring(src_bitstring, index_one) \
                and is_index_valid_on_bitstring(src_bitstring, index_two):
            if index_one != index_two:
                lst = list(src_bitstring)
                lst[index_one], lst[index_two] = lst[index_two], lst[index_one]
                for item in lst:
                    new_string += item
            else:
                raise BitUtilityFunctionError("Indices for bit swapping " +\
                        "are identical.", location=_ERROR_LOCATION_)
        else:
            raise BitUtilityFunctionError("Indices for bit swapping " +\
                    "are out of range", location=_ERROR_LOCATION_)
    else:
        raise BitUtilityFunctionError(validator.get_errors(),
                                      location=_ERROR_LOCATION_)
    return new_string
