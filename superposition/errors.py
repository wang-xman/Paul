"""
MODULE

superposition.errors.py

PATH

[app_root]/superposition/errors.py

INTRO

Dedicated errors in package.

CONTENT

LOG

Updated on 28 September 2021 | Created on 18 April 2021
"""
from .base import SuperpositionBaseValidationError, SuperpositionBaseError


class SuperlistValidationError(SuperpositionBaseValidationError):
    header = 'Superlist_Validation_Error'


class SuperpositionError(SuperpositionBaseError):
    header = 'Superpostion_Error'


class SuperpositionValidationError(SuperpositionBaseValidationError):
    header = 'Superpostion_Validation_Error'
