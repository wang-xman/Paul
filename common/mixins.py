#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.mixins.py

PATH

[app_root]/common/mixins.py

INTRO

Common mixin classes used in class design.

CONTENT

`Non_Instantiable_Mixin` - Mixin to prevent a class from
instantiation

`Non_Subclassable_Mixin` - Mixin to prevent a class from
being subclassed; to be inserted into the metaclass

LOG

Updated on 29 September 2021 | Created on 29 September 2021
"""

_MODULE_LOCATION_= 'common.mixins'


class Non_Instantiable_Mixin:
    """ Prevent instantiation

    WARNING Even subclass of this class can not be
    instantiated.
    """
    def __new__(cls, *args, **kwargs):
        if cls:
            raise TypeError("Class '{}' ".format(cls.__name__) +\
                "may not be instantiated")
        return super().__new__(cls, *args, **kwargs)


class Non_Subclassable_Mixin:
    """ Prevent subclassing

    Mixin to be inserted into a metaclass.
    """
    def __new__(cls, clsname, clsbases, clsdict):
        for base_class in clsbases:
            if isinstance(base_class, cls):
                raise TypeError("Type '{0}' ".format(base_class.__name__) +\
                        "must not be subclassed.")
        return super().__new__(cls, clsname, clsbases, dict(clsdict))
