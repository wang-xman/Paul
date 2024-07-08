"""
SUBPACK

Matrix object

PATH

[app_root]/linear_space/matrix/

INTRO

Various types of matrices.

LOG

Updated on 24 September 2021 | Created on 15 November 2020
"""
from .matrix import Matrix
from .square_matrix import SquareMatrix
from .identity_matrix import IdentityMatrix
# special matrices
from .special import SINGLE_IDENTITY, HADAMARD, STATE_ONE_PROJECTION, \
    STATE_ZERO_PROJECTION, PAULI_X, PAULI_Y, PAULI_Z, \
    ROTATE_HALF_PI_ON_X, ROTATE_HALF_PI_ON_Y
