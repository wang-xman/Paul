#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.matrix.special.py

PATH

[app_root]/linear_space/matrix/special.py

INTRO

Specialised matrix objects.

CONTENT

`HADAMARD` - Walsh-Hadamard matrix, a `SquareMatrix` instance

`STATE_ZERO_PROJECTION` - projection matrix [[1,0],[0,0]],
a `SquareMatrix` instance

`STATE_ONE_PROJECTION` - projection matrix [[0,0],[0,1]],
a `SquareMatrix` instance

`PAULI_X/Y/Z` - Pauli matrices

`ROTATE_HALF_PI_ON_X` - rotate a spin around the x-axis by pi/2;
a `SquareMatrix` instance

`ROTATE_HALF_PI_ON_Y` - rotate a spin around the y-axis by pi/2;
a `SquareMatrix` instance

LOG

Updated on 02 October 2021 | Created on 15 November 2020
"""
from linear_space.numpy_lib import np_array, np_sqrt
from .square_matrix import SquareMatrix
from .identity_matrix import IdentityMatrix


SINGLE_IDENTITY = IdentityMatrix()
""" Single bit identity matrix """


HADAMARD = SquareMatrix(array=np_array([
    [1.0/np_sqrt(2.0), 1.0/np_sqrt(2.0)], [1.0/np_sqrt(2.0), -1.0/np_sqrt(2.0)]
]))
""" Hadamard matrix 2-by-2 """


STATE_ZERO_PROJECTION = SquareMatrix(array=np_array([[1, 0], [0, 0]]))
""" Projection operator |0><0| """

STATE_ONE_PROJECTION = SquareMatrix(array=np_array([[0, 0], [0, 1]]))
""" Projection operator |1><1| """


PAULI_X = SquareMatrix(array=np_array([[0, 1], [1, 0]]))
""" Pauli matrix x """

PAULI_Y = SquareMatrix(array=np_array([[0, 0. - 1.j], [0. + 1.j, 0]]))
""" Pauli matrix y """

PAULI_Z = SquareMatrix(array=np_array([[1, 0], [0, -1]]))
""" Pauli matrix z """


ROTATE_HALF_PI_ON_X = SquareMatrix(array=np_array([
    [1/np_sqrt(2.0), 1.0j/np_sqrt(2.0)], [1.0j/np_sqrt(2.0), 1/np_sqrt(2.0)]
]))
""" Rotate spin around x-axis by pi/2 """

ROTATE_HALF_PI_ON_Y = \
        SquareMatrix(array=np_array([[1, 1], [-1, 1]]) / np_sqrt(2.0))
""" Rotate spin around y-axis by pi/2 """
