"""
MODULE

linear_space.linear_object.validators.py

PATH

[app_root]/linear_space/linear_object/validators.py

INTRO

Validators

CONTENT

`LinearObjectValidator`

LOG

Updated on 02 October 2021 | Created on 27 September 2021
"""
from linear_space.numpy_lib import np_ndarray
from linear_space.base import LinearSpaceBaseValidator
from linear_space.number import is_number
from .errors import LinearObjectValidationError

_MODULE_LOCATION_ = 'linear_space.linear_object.validators'


class LinearObjectSubarrayValidator(LinearSpaceBaseValidator):
    """ Validate subarray of a linear object """
    error_class = LinearObjectValidationError
    error_location = _MODULE_LOCATION_ + '.LinearObjectSubarrayValidator'

    def __init__(self, array=None):
        super().__init__()
        self.validate_subarray_type(array=array)
        # If no error, validate subarray dimension
        if len(self.get_errors()) == 0:
            self.validate_subarray_dimension(array=array)
        # If no error, validate subarray element type
        if len(self.get_errors()) == 0:
            self.validate_subarray_element_type(array=array)

    def validate_subarray_type(self, array=None):
        """ Each subarray must be `numpy.ndarray` """
        wrong_type_counter = 0
        for _ , subarray in enumerate(array):
            if not isinstance(subarray, np_ndarray) :
                wrong_type_counter += 1
        if wrong_type_counter > 0:
            self.report_errors('Subarray in the array passed in is ' +\
                    'not numpy ndarray object.')

    def validate_subarray_dimension(self, array=None):
        """ Each subarray must be of dimension 1

        Subarray `ndim` property must return 1
        """
        wrong_dim_counter = 0
        for _ , subarray in enumerate(array):
            if subarray.ndim != 1:
                wrong_dim_counter += 1
            # subarray is indeed 1D
            else:
                if len(subarray) == 0:
                    self.report_errors('Subarray is empty')
        if wrong_dim_counter > 0:
            self.report_errors('Subarray(s) in the array passed in ' +\
                   'is(are) not one-dimensional numpy array(s).')

    def validate_subarray_element_type(self, array=None):
        """ Elements of subarray must be number """
        non_numeric_counter = 0
        for _ , subarray in enumerate(array):
            for el in subarray:
                if not is_number(el):
                    non_numeric_counter += 1
        if non_numeric_counter > 0:
            self.report_errors('Subarray(s) in the array passed in ' +\
                   'contain non-numeric elements.')


class LinearObjectValidator(LinearSpaceBaseValidator):
    """ Linear object validator

    Linear object is initialised with a 2D numpy array
    of numbers and each subarray must be 1D.
    """
    error_class = LinearObjectValidationError
    error_location = _MODULE_LOCATION_ + '.LinearObjectValidator'

    def __init__(self, array=None):
        super().__init__()
        self._validated_array = None
        self.validate(array=array)
        if len(self.get_errors()) == 0:
            self._validated_array = array

    def validate(self, array=None):
        if array is None:
            self.report_errors('To instantiate a linear object, ' +\
                    'please provide a numpy array.')
        elif not isinstance(array, np_ndarray):
            self.report_errors('To instantiate a linear object, ' +\
                    'a two-dimensional numpy array of numbers is needed.')
        elif array.ndim != 2:
            self.report_errors('The numpy array passed to ' +\
                    'instantiate linear object is not a ' +\
                    'two-dimensional array.')
        else:
            pass
        # validation chain
        subarray_validator = LinearObjectSubarrayValidator(array=array)
        if not subarray_validator.is_valid:
            self.report_errors(subarray_validator.get_errors())

        # fill validated data
        if len(self.get_errors()) == 0:
            self._validated_array = array

    def validated_data(self):
        return {
            'array': self._validated_array
        }
