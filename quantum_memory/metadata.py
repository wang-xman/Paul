#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.metadata.py

PATH

[app_root]/quantum_memory/metadata.py

INTRO

Metadata is an object that extracts information about
another object which is referred to as 'referenced object',
i.e. data that describes data.

In gate-based quantum simulator, metadata delivers
computational advantage, as the matrices of gate operators
are usually constructed based on global property of qubit
states, such as number of qubits (noq), control index,
target index, etc. These properties can be acquired a prior
the actual loading of the underlying qubit state vector.
This helps us delay most computation-intensive tasks to the
lastest stage, or lazy loading.

Class `BaseRegisterMetadata` is a metadata class for generic
quantum register. It only extracts the most common properties
(metadata) of register, such as label and register type.
Specialised register metadata class must subclass from it.

CONTENT

`BaseRegisterMetadata` - Qubit register metadata object

LOG

Updated on 01 October 2021 | Created on 11 August 2021
"""
from quantum_register.base_register import BaseRegister
from .errors import RegisterMetadataError

_MODULE_LOCATION_ = 'quantum_memory.metadata'


class BaseRegisterMetadata:
    """ Register metadata base class

    Register metadata is a wrapping class that holds
    reference to a register - referenced register -
    and extracts metadata of it.

    In case the internal state in the referenced register
    has changed, for example, register takes in a different
    state, the related metadata properties change, too.

    Metadata collects the following information about the
    referenced register,

    `self._register` : instance of `BaseRegister` class;
    the referenced register

    `self.label` : string, register's label

    `self.register_type` : string, class name of register's
    class

    In addition to the aforementioned properties, there are
    getters and setters,

    `self.get_register()` : returns the internal referenced
    register instance

    `self.set_register(,new_register)` : replaces the referenced
    register by a new one

    `self.as_dict()` : returns a dictionary that contains
    the basic properties of the referenced register
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.BaseRegisterMetadata'

    def __init__(self, register):
        """ Register Metadata : Init """
        if isinstance(register, BaseRegister):
            self._register = register
        else:
            raise RegisterMetadataError("Register metadata " +\
                    "object references only to register that is an " +\
                    "instance of BaseRegister or its subclasses.",
                    location=self._ERROR_LOCATION_+'.__init__')

    @property
    def label(self):
        """ Base Register Metadata : Returns register label """
        return self._register.label

    @property
    def register_type(self):
        """ Base Register Metadata : Returns register type """
        return self.get_register().__class__.__name__

    def get_register(self):
        """ Base Register Metadata : Returns referenced register """
        return self._register

    def set_register(self, new_register):
        """ Base Register Metadata : Manually replace register

        NOTE This method manually replaces the referenced register.
        Use with caution.

        Arguements

        `new_register` : a register instance used to replace the
        existing one
        """
        if isinstance(new_register, BaseRegister):
            self._register = new_register
        else:
            raise RegisterMetadataError("Register metadata object " +\
                    "can only reference a register that is an instance " +\
                    "of BaseRegister or its subclasses.",
                    location=self._ERROR_LOCATION_+'.set_register')

    def as_dict(self):
        """ Base Register Metadata : Converts object into a dict """
        metadata_dict = {
            'label': self.label,
            'register_type': self.register_type
        }
        return metadata_dict
