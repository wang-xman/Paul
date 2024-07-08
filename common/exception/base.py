#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.exception.base.py

PATH

[app_root]/common/exception/base.py

INTRO

Application-wide base error and exception.

All exceptions or errors used in the application must
subclass from `BaseError` class.

CONTENT

`Base_Error` - Base class to all errors in application

LOG

Updated on 28 September 2021 | Created on 15 November 2020
"""
_MODULE_LOCATION_ = 'common.exception.base.py'


class Base_Error(Exception):
    """ Base error class

    Errors and exceptions declared in the application must
    subclass from this base.

    Subclass may implement `header`, `location` and `level`
    class attributes to enrich the message upon being raised.

    Subclass may override the `stringify` method to customise
    error message.

    CONSTRUCTOR

    `message` (`str`) : error message passed in as a tring;
    if `None` or not a string, `Exception` is triggered

    `location` (`str`) : location where error is reported;
    if provided, it overrides the default error location
    specified by class attribute `cls.location` and it is
    appended in list of report location

    ATTRIBUTES

    `self.__raw_message` (`str`) : raw message given by the
    caller as a string

    `self.__report_location` (`list`) : error locations given
    per instantiation or relocation; same error instance can
    propagate to down-stream callers; tracking locations
    helps locate the propagation route of the error

    `self.__stringified_location` : property; returns stringified
    locations chained using arrow symbol (->)

    `self.stringify()` : stringify error messages

    `self.message` (`str`) : raw message of error

    `self.full_message` (`str`) : full message; header, location
    and level information, should they be available, are included;
    calls `stringify()` to return the full message

    `self.report_location` (`str`) : locations where error was
    reported; returns a string with locations chained using
    arrows (->)

    `self.first_location` (`str`) : first location the error
    was reported; first item in the report location list

    `self.last_location` (`str`) : last location the error was
    reported; last in the list

    `self.__str__()` : calls `stringify()` to get a customised
    string
    """
    def __new__(cls, *args, **kwargs):
        """ Base_Error :: new

        Prevent direct instantiation
        """
        if cls is Base_Error:
            raise TypeError("Base_Error class must not " +\
                    "be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, message, location=None):
        """ Base_Error :: init

        Argument

        `message` (`str`) : error message passed in as a tring;
        if `None` or not a string, `Exception` is triggered

        `location` (`str`) : location where error is reported;
        if provided, it overrides the default error location
        specified by class attribute `cls.location` and it is
        appended in list of report location
        """
        self.__report_location = []
        if message is not None:
            if isinstance(message, str):
                self.__raw_message = message
                super().__init__(message)
                # location overrides the class attribute
                # `cls.location` of subclass
                if location is not None:
                    if isinstance(location, str):
                        self.__report_location.append(location)
                    else:
                        raise Exception('Error location must be a string.')
                # no location provided
                else:
                    # check if default location exists
                    if getattr(self, 'location', None):
                        self.__report_location.append(self.location)
                    else:
                        try:
                            # if module location exists, use it
                            self.__report_location.append(_MODULE_LOCATION_)
                        except NameError:
                            self.__report_location.append('UNREPORTED')
            else:
                raise Exception('Error message must be a string.')
        else:
            raise Exception('Error instance must contain a message.')

    @property
    def __stringified_location(self):
        """ Base_Error :: Construct a location string

        All locations are chained using '->' symbol.

        Earliest report location is at the left most position
        and arrow (->) indicates the propogation direction.
        """
        location_string = ''
        if len(self.__report_location) == 0:
            location_string = location_string + 'UNREPORTED'
        else:
            for idx, loc in enumerate(self.__report_location):
                # also include the case with only 1 loc
                if idx == len(self.__report_location) - 1:
                    location_string = location_string + loc
                elif idx == 0:
                    location_string = location_string + loc + "\n\t"
                else:
                    location_string = location_string + " -> " + loc + "\n\t"
        return location_string

    def stringify(self):
        """ Base_Error :: Prepare full error message

        Full message consists of header, message body,
        error location (if applicable), and level
        (if applicable).

        Return

        `fullmsg` (`str`) : a string represents the full
        error message
        """
        fullmsg = ''
        if hasattr(self, 'header') and not self.header is None:
            if self.__raw_message is None:
                fullmsg = self.header
            else:
                fullmsg = self.header + ":\n\t" + '\t MESSAGE: ' +\
                        self.__raw_message
        else:
            fullmsg = self.__raw_message
        # error location
        fullmsg = fullmsg + "\n\t" + '\t LOCATIONS:' +\
                self.__stringified_location
        # add error level
        if getattr(self, 'level', None):
            fullmsg = fullmsg + "\n\t" + "\t LEVEL: " + self.level
        return fullmsg

    @property
    def message(self):
        """ Base_Error :: Raw message """
        return self.__raw_message

    @property
    def full_message(self):
        """ Base_Error :: Fully formated error mesaage """
        return self.stringify()

    @property
    def report_location(self):
        """ Base_Error :: Return reported locations

        All locations are chained using arrow symbol (->).
        """
        return self.__stringified_location

    @property
    def first_location(self):
        """ Base_Error :: Return first report location """
        return self.__report_location[0]

    @property
    def last_location(self):
        """ Base_Error :: Return last report location """
        return self.__report_location[-1]

    def relocate(self, location):
        """ Base_Error :: Append a new location

        Relocation method is useful when bubbling an error
        and to identify the latested location where error
        is reported.
        """
        if location is not None and isinstance(location, str):
            self.__report_location.append(location)
        else:
            raise Exception(message="New location assigend to " +\
                    "an error instance must be a string.")
        return self

    def __str__(self):
        """ Base_Error :: String shown while being `raise` """
        return "\n\t" + self.stringify()
