"""
PACKAGE

Superposition package

PATH

[app_root]/superposition/

INTRO

Superposition introduced in this package is a generic
class that implements the minimal number of common
properties. Most importantly, generic superposition
wraps a superlist which satisfies a set of criteria.

LOG

Updated on 02 October 2021 | Created on 17 April 2021
"""
from .validators import SuperlistValidator, SuperpositionValidator
from .superposition import Superposition
