#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.validators.py

PATH

[app_root]/linear_space/vector/validators.py

INTRO

Base vector class implements common properties to
all vector objects. Most importantly, base vector
class defines the shape of vector, i.e. either
one column or one row.

CONTENT


LOG

Updated on 30 September 2021 | Created on 07 November 2020
"""
from linear_space.numpy_lib import np_complex
from linear_space.number import VALID_NUMERIC_TYPES, is_integer
from linear_space.base import LinearSpaceBaseValidator
from linear_space.linear_object.linear_object import LinearObjectValidator

from .errors import VectorValidationError, ColumnVectorValidationError, \
    StandardBasisVectorValidationError, RowVectorValidationError

_MODULE_LOCATION_ = 'linear_space.vector.validators'


class BaseVectorInitValidator(LinearObjectValidator):
    """ Base vector init validator """
    error_class = VectorValidationError
    error_location = _MODULE_LOCATION_ + '.BaseVectorInitValidator'

    def __init__(self, array=None):
        super().__init__(array=array)
        if len(self.get_errors()) == 0:
            self.validate_dimension(array=array)
        if len(self.get_errors()) == 0:
            self._validated_array = array

    def validate_dimension(self, array=None):
        if len(array) == 1: # row like
            if len(array[0]) == 1:
                self.report_errors('Array passed in to instantiate' +\
                        'a vector is in fact a scalar.')
        elif len(array) > 1: # column like
            if len(array[0]) != 1:
                self.report_errors('Array passed in to instantiate' +\
                        'a vector is neither row-like nor column-like.')
        else:
            pass


class ColumnVectorInitValidator(BaseVectorInitValidator):
    """ Validate an numpy array for column vector

    Validated array must be a column-like vector stored as
    an array of lists and each list contains a single number.
    For example [[1],[2],[3],[4]], which can be obtained by
    perform a transpose on the 1D array.
    """
    error_class = ColumnVectorValidationError
    error_location = _MODULE_LOCATION_ + '.ColumnVectorValidator'

    def __init__(self, array=None, datatype=None):
        super().__init__(array=array)
        if self.is_valid:
            self.validate_one_column(array=array)
            if datatype is not None:
                self.validate_datatype(datatype)
        if self.is_valid:
            # no datatype specified, default to np.complex
            if datatype is None:
                self._validated_array = array.astype(np_complex)
            else:
                self._validated_array = array.astype(datatype)

    def validate_one_column(self, array=None):
        if len(array) < 2:
            self.report_errors('A column vector must have at least two rows.')
        elif len(array[0]) != 1:
            self.report_errors('Each row of a column vector must '+\
                    'contain exactly one number')
        else:
            pass

    def validate_datatype(self, datatype):
        """ Validate datatype """
        if not datatype in VALID_NUMERIC_TYPES:
            self.report_errors('Unknown datatype')


class StandardBasisVectorInitValidator(LinearSpaceBaseValidator):
    """ Standard basis vector validator

    Index location is the location of the only non-zero element
    in the vector, and it is a scientific index starting from 0.
    Size of the unit vector must be at least 2. Validated data
    is a dictionary that has two keys,
        {
            'iloc':
            'size':
        }

    CONSTRUCTOR

    `iloc` (`int`): index location of the only nonzero element;
    in scientific indexing starting from 0

    `size` (`int`): size, or number of elements, of the vector.
    """
    error_class = StandardBasisVectorValidationError
    error_location = _MODULE_LOCATION_ + '.StandardBasisVectorValidator'

    def __init__(self, iloc=None, size=None):
        super().__init__()
        self._validated_iloc = None
        self._validated_length = None
        self.validate(iloc=iloc, size=size)
        if len(self.get_errors()) == 0:
            self._validated_iloc = iloc
            self._validated_size = size

    def validate(self, iloc=None, size=None):
        local_errors = []
        if not is_integer(iloc) or not is_integer(size):
            local_errors.append("Index location or size is not " +\
                "integer. Both arguments must be integers.")
        else:
            if size < 2:
                local_errors.append("Size of a standard basis " +\
                    "is smaller than 2.")
            else:
                if iloc < 0:
                    local_errors.append("Index out of range. Index of the " +\
                            "only nonzero entry of a standard basis " +\
                            "is negative.")
                elif iloc > size - 1:
                    local_errors.append("Index out of range. Index " +\
                            "of the only nonzero entry of a standard " +\
                            "basis must be smaller than the size of " +\
                            "the vector less 1.")
                else:
                    pass

        if len(local_errors) > 0:
            self.report_errors(message=local_errors)

    def validated_data(self):
        ret = {
            'iloc': self._validated_iloc,
            'size': self._validated_size
        }
        return ret


class RowVectorInitValidator(BaseVectorInitValidator):
    """ Row vector validator """
    error_class = RowVectorValidationError
    error_location = _MODULE_LOCATION_ + '.RowVectorValidator'

    def __init__(self, array=None, datatype=None):
        super().__init__(array=array)
        if self.is_valid:
            self.validate_one_row(array=array)
            if datatype is not None:
                self.validate_datatype(datatype)
        if self.is_valid:
            # no datatype specified, default to np.complex
            if datatype is None:
                self._validated_array = array.astype(np_complex)
            else:
                self._validated_array = array.astype(datatype)

    def validate_one_row(self, array=None):
        if len(array) != 1:
            self.report_errors('A row vector must have exactly one row.')
        elif len(array[0]) <= 1:
            self.report_errors('A row vector must contain more than '+\
                    'one element.')
        else:
            pass

    def validate_datatype(self, datatype):
        """ Validate datatype """
        if not datatype in VALID_NUMERIC_TYPES:
            self.report_errors('Unknown datatype')
