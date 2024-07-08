#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.function.validators.py

PATH

[app_root]/common/function/validators.py

INTRO

Validator for subpack

CONTENT

LOG

Updated on 22 September 2021 | Created on 19 December 2020
"""
from common.validator import Base_Validator
from common.string import is_string, is_empty_string, has_space

from .errors import SkipListValidationError

_MODULE_LOCATION_ = 'common.function.validators'


class SkipListValidator(Base_Validator):
    """ Validate function signature skiplist """
    error_class = SkipListValidationError
    error_location = _MODULE_LOCATION_ + '.SkipListValidator'

    def __init__(self, skip_list=None):
        super().__init__()
        if isinstance(skip_list, list):
            # if not empty
            if not len(skip_list) == 0:
                for argname in skip_list:
                    if not is_string(argname):
                        self.report_errors('Function argumnet ' +\
                                'skiplist contains non-string element. ' +\
                                'This is forbidden.',
                                location=self.error_location+'.__init__')
                    elif is_empty_string(argname):
                        self.report_errors('Function argumnet ' +\
                                'skiplist contains empty string. ' +\
                                'This is forbidden.',
                                location=self.error_location+'.__init__')
                    elif has_space(argname):
                        self.report_errors('Function argumnet ' +\
                                'skiplist contains argument name string ' +\
                                'that has space. This is forbidden.',
                                location=self.error_location+'.__init__')
                    else:
                        pass
        else:
            self.report_errors('Function argumnet skiplist is not a list.',
                    location=self.error_location+'.__init__')
