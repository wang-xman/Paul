#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.standard_basis.py

PATH

[app_root]/linear_space/vector/standard_basis.py

INTRO

Standard basis vector is a subclass of unit vector.

CONTENT

`StandardBasisVector` - Standard basis vector such as
    `[[0]
      [1]
      [0]]`
and it is a special case and hence a subclass of `UnitVector`

LOG

Updated on 30 September 2021 | Created on 07 November 2020
"""
from linear_space.numpy_lib import np_transpose, np_zeros
from .unit_vector import UnitVector
from .validators import StandardBasisVectorInitValidator

_MODULE_LOCATION_ = 'linear_space.vector.standard_basis'


class StandardBasisVector(UnitVector):
    """ Standard basis vector

    Standard basis - also known as natural basis - is a
    specialised unit vector of which the internal array
    has only one nonzero element and the value of that
    element is 1, such as (1,0,0).

    Index location (`iloc`) is the location of the nonzero
    element. Elements are indexed using scientific index
    starting from 0. As a generic vector, size of the vector
    is not necessarily a power of 2 and is thus not always
    having a binary interpretation (equivalent).

    CONSTRUCTOR

    `iloc` (`int`): location of the only nonzero element in
    vector; it starts from 0

    `size` (`int`): size the unit vector; also the total
    number of elements in the vector; must to greater than
    1 (>= 2)

    ATTRIBUTES

    `self._index_location` (`int`): index of the only nonzero
    entry in the basis, i.e. index location

    `self.iloc`: property; returns `self._index_location`

    `self.string_representation()`: returns the basis in the format
    of, for example
        [1.00
         0.00
         0.00]
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.StandardBasisVector'

    def __init__(self, iloc=None, size=None):
        """ Standard Basis :: Initialiser """
        validator = StandardBasisVectorInitValidator(iloc=iloc, size=size)
        if validator.is_valid:
            vd = validator.validated_data()
            self._index_location = vd['iloc']
            array = np_zeros(vd['size'])
            array[self._index_location] = 1.0
            # Inherits from base class.
            super().__init__(array=np_transpose([array]))
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    @property
    def iloc(self):
        """ Standard Basis :: Returns index location """
        return self._index_location

    def string_representation(self):
        """ Standard Basis :: String for basis vector

        Only real part is needed and only 1 decimal point is shown.
        """
        vector_size = len(self.as_array())
        fullstring = "\n["
        for i, item in enumerate(self.as_array()):
            if i == 0:
                fullstring += "{c.real:.1f}\n".format(c=item[0])
            elif i != vector_size - 1:
                fullstring += " {c.real:.1f}\n".format(c=item[0])
            else:
                fullstring += " {c.real:.1f}".format(c=item[0])
        fullstring += "]\n"
        return fullstring
