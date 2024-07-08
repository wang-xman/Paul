#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

superposition.base.py

PATH

[app_root]/superposition/base.py

INTRO

Detailed explanation of superposition can be found in
superposition module.

CONTENT

Base classes used in superposition application

LOG

Updated on 30 September 2021 | Created on 17 April 2021
"""
from abc import ABC, abstractmethod, abstractproperty
from common.exception import Generic_Error, Validation_Error
from common.validator import Base_Validator


class AbstractSuperposition(ABC):
    """ Superposition abstract class

    Any superposition must implement the following
    properties and methods.
    """

    @abstractproperty
    def component_type(self):
        pass

    @abstractmethod
    def as_superlist(self):
        pass


class SuperpositionBaseError(Generic_Error):
    header = 'Superposition_Base_Error'


class SuperpositionBaseValidationError(Validation_Error):
    header = 'Superposition_Base_Validation_Error'


class SuperpositionBaseValidator(Base_Validator):
    error_class = SuperpositionBaseValidationError
