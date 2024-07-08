#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
SUBPACK

Application-wide base validator

PATH

[app_root]/common/validator/

INTRO

Application-wide base validator must not be instantiated.
Any validator used in this application must subclass from
this base validator

LOG

Updated on 30 September 2021 | Created on 22 September 2021
"""
from .base_validator import Base_Validator
