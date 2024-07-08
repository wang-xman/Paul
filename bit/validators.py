#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.validator.py

PATH

[app_root]/bit/validator.py

INTRO

Bit object validators are frequently used to validate
bit objects such as bitstring and bitlist.

NOTE Bitrange bound and bitrange are different. The former
is used in the later; bitrange requires the total number of
bits (nob).

LOG

Updated on 05 October 2021 | Created on 06 November 2020
"""
from linear_space.numpy_lib import np_ndarray, np_array, np_intc
from linear_space.number import is_number
from linear_space.utils import maximum, minimum, has_only_integer

from .base import BitBaseValidator
from .errors import BitarrayValidationError, BitstringValidationError, \
    BitlistValidationError, \
    BitrangeBoundValidationError, BitrangeValidationError

_MODULE_LOCATION_ = 'bit.validators'


class BitarrayValidator(BitBaseValidator):
    """ Validate bitarray """
    error_class = BitarrayValidationError
    error_location = _MODULE_LOCATION_ + '.BitarrayValidator'

    def __init__(self, bitarray=None):
        super().__init__()
        self._validated_array = None
        self.validate(value=bitarray)

    def validate(self, value=None):
        validated_list = []
        if value is None or len(value) == 0:
            self.report_errors("Bitarray is not provided.")
        else:
            if not type(value) in [np_ndarray, list]:
                self.report_errors("Bitarray is neither a " +\
                        "numpy.ndarray nor a list.")
            else:
                for _ , digit in enumerate(value):
                    if not digit in [0, 1]:
                        self.report_errors(
                                "Element in bitarray is unrecognised.")
                    else:
                        validated_list.append(np_intc(digit))

        if len(self.get_errors()) == 0:
            self._validated_array = np_array(validated_list, dtype=np_intc)

    def validated_data(self):
        ret = {
            'bitarray': self._validated_array
        }
        return ret


class BitstringValidator(BitBaseValidator):
    """ Bitstring validator

    A bitstring contains only '0' or '1' or both
    and it cannot be empty.
    """
    error_class = BitstringValidationError
    error_location = _MODULE_LOCATION_ + '.BitstringValidator'

    def __init__(self, bitstring=None):
        super().__init__()
        self._validated_value = None
        self.validate(value=bitstring)

    def validate(self, value=None):
        if value is None:
            self.report_errors("Bitstring is not provided.")
        else:
            # Check if a string
            if not isinstance(value, str):
                self.report_errors("Bitstring is not a string.")
            else:
                # string must not be empty
                if len(value) == 0 or value.isspace():
                    self.report_errors("Bitstring is empty.")
                else:
                    for char in list(value):
                        if not char in set(['0','1']):
                            self.report_errors("Bitstring contains " +\
                                "symbol(s) other than '0' and '1'.")
        if len(self.get_errors()) == 0:
            self._validated_value = value

    def validated_data(self):
        ret = {
            'bitstring': self._validated_value
        }
        return ret


class BitlistValidator(BitBaseValidator):
    """ Bitlist validator

    Bitlist is a list of tuples.

    In each tuple, the first element is a number
    (referred to as 'amplitude') and the second one
    is a bitstring (referred to as 'component').
    For example
        [(0.5, '00'), (0.5,'11'), (0.5,'10')]
    is a valid bitlist.

    A bitlist must meet the following criteria:

    [1] List must not be empty. Bitlist is allowed to
    contain only one tuple.

    [2] Each element in bitlist is a tuple of exactly
    two elements.

    [3] First element in tuple must be a number.

    [4] Second element in tuple must be a bitstring.

    [5] All bitstrings must have the same length.

    NOTE Bitlist is actually a realisation of a superlist.
    """
    error_class = BitlistValidationError
    error_location = _MODULE_LOCATION_ + '.BitlistValidator'

    def __init__(self, bitlist=None):
        super().__init__()
        self.validate(bitlist)

    def validate_tuple_amplitude(self, amplitude):
        """ Validate amplitude in tuple

        Amplitude must be numeric.
        """
        if not is_number(amplitude):
            self.report_errors("Bitlist contains amplitude(s) that " +\
                    "is(are) not numberic.")

    def validate_tuple_bitstring(self, bs):
        """ Validate bitstring in tuple

        Second element in tuple must be valid bit string.
        """
        bs_validator = BitstringValidator(bitstring=bs)
        if not bs_validator.is_valid:
            self.report_errors(bs_validator.get_errors(),
                               location=self.error_location)

    def validate_tuple(self, member_tuple):
        """ Validate member tuple """
        if isinstance(member_tuple, tuple):
            # tuple not empty
            if len(member_tuple) != 0:
                if len(member_tuple) == 2:
                    # Validate amplitude
                    self.validate_tuple_amplitude(member_tuple[0])
                    # Validate bitstring
                    self.validate_tuple_bitstring(member_tuple[1])
                else:
                    self.report_errors("Tuple in bitlist doesn't " +\
                            "have exactly two elements.")
            # tuple empty
            else:
                self.report_errors('Bitlist contains empty tuple.')
        else:
            self.report_errors("Element in bitlist is not a tuple.")

    def validate(self, bitlist):
        # Validate overal structure
        if not isinstance(bitlist, list):
            self.report_errors("Bitlist is not a list.")
        elif len(bitlist) == 0:
            self.report_errors("Bitlist is empty.")
        else:
            # Validate each tuple
            for member in bitlist:
                self.validate_tuple(member)
        # if all good, last check length of bitstrings
        if self.is_valid:
            if len(set(len(tp[1]) for tp in bitlist)) > 1:
                self.report_errors("Bitstrings in list have " +\
                                   "different lengths.")


class BitrangeBoundValidator(BitBaseValidator):
    """ Validate bitrange bounds

    Bitrange bound is a list of two positve integers,
    such as [5,10], which set the lower- and upper
    bounds of a range.

    Bitrange is instantiated with a bound.

    Both integers are scientific indices and compatible
    with total number of bits.

    If the first integer is less than the second, such as
    [5,10], this range is considered in 'normal order',
    opposite to the 'reversed' order, for example, [10,5].

    Use of list coincides with the mathematical convention
    that a range presented in a square brackets includes
    values at the boundaries, i.e. range [2, 10] includes
    2 and 10.

    NOTE Bound validator does NOT validate if bound is
    compatible with number of bits.

    CONSTRUCTOR

    `number_of_bits` (`int`) : total number of bits for
    which the bitrange is mapped

    `bound` (`list`) : a list of two integers that defines
    lower and upper bounds of intended range
    """
    error_class = BitrangeBoundValidationError
    error_location = _MODULE_LOCATION_ + '.BitrangeBoundValidator'

    def __init__(self, bound=None):
        super().__init__()
        self.validate(bound=bound)

    def validate_bound_elements(self, bound):
        """ Valdiate bitrange limits """
        if not has_only_integer(bound):
            self.report_errors("Bitrange bound contains non-integers.")
        # can't have negative values
        elif bound[0] < 0 or bound[1] < 0:
            self.report_errors("Bitrange bound contains " +\
                    "negative value(s).")
        else:
            pass

    def validate(self, bound=None):
        """ Main validate method """
        if not isinstance(bound, list):
            self.report_errors("Bitrange bound is not as a list.")
        elif len(bound) != 2:
            self.report_errors("Bitrange bound doesn't have " +\
                    "exactly two elements.")
        # a list of two elements
        else:
            self.validate_bound_elements(bound)


class BitrangeValidator(BitrangeBoundValidator):
    """ Bitrange validator

    Bitrange validator requires the total number of
    bits.
    """
    error_class = BitrangeValidationError
    error_location = _MODULE_LOCATION_ + '.BitrangeValidator'

    def __init__(self, number_of_bits=None, bound=None):
        super().__init__(bound=bound)
        if self.is_valid:
            self.validate_nob(nob=number_of_bits, bound=bound)

    def validate_nob(self, nob=None, bound=None):
        if minimum(bound) > nob - 1 or maximum(bound) > nob - 1:
            self.report_errors("Bitrange bound is out of range.")
