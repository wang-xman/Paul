"""
MODULE

superposition.validators.py

PATH

[app_root]/superposition/validators.py

INTRO

Dedicated validators

CONTENT

`SuperlistValidator`

`SuperpositionValidator`

LOG

Updated on 02 October 2021 | Created on 18 April 2021
"""
from linear_space.number import is_number
from .base import SuperpositionBaseValidator
from .errors import SuperlistValidationError, SuperpositionValidationError

_MODULE_LOCATION_ = 'superposition.validators'


class SuperlistValidator(SuperpositionBaseValidator):
    """ Validate a generic superlist

    A superlist is a list of tuples.

    First element of each tuple is often referred to
    as 'amplitude'. The second element is 'component'.
    Tuple is usually referred to as 'member'.

    In this terminology, a superlist looks like
        `[member, member, ...]`
    and each member is (amplitude, component).

    A superlist must meet the following criteria:

    [1] List must not be empty. Superlist is allowed
    to have just one item, i.e. one tuple.

    [2] In the list, each element must be a tuple of
    exactly two elements.

    [3] All first elements in the tuples must be of
    the same type. In quantum mechanics, the first
    element is usually required to be number.

    [4] All second elements in the tuples must of the
    same type. NOTE Can't validate it here especially
    if components are subclasses of certain type.
    Further validation will have to be implemented in
    superposition object.
    """
    error_class = SuperlistValidationError
    error_location = _MODULE_LOCATION_ + '.SuperlistValidator'

    def __init__(self, superlist=None):
        """ Superlist Validator :: Initialiser """
        super().__init__()
        self.validate(superlist)

    def validate_member_tuple(self, member):
        if isinstance(member, tuple):
            # tuple not empty
            if len(member) != 0:
                if len(member) == 2:
                    # 1st element in tuple must be numeric
                    if not is_number(member[0]):
                        self.report_errors("Superlist contains " +\
                                "amplitude(s) that is(are) not " +\
                                "numeric.")
                else:
                    self.report_errors("Tuple in superlist " +\
                            "doesn't have exactly two elements.")
            # tuple empty
            else:
                self.report_errors('Superlist contains empty tuple(s).')
        else:
            self.report_errors("Element in the superlist is not a tuple.")

    def validate(self, superlist):
        """ Superlist Validator :: Main """
        # 1. validate overal structure
        if not isinstance(superlist, list):
            self.report_errors("Superlist is not a list.")
        elif isinstance(superlist, list) and len(superlist) == 0:
            self.report_errors("Superlist is empty.")
        else:
            # 1. Ensure each element in the list is a tuple of two elements
            for item in superlist:
                self.validate_member_tuple(item)


class SuperpositionValidator(SuperpositionBaseValidator):
    """ Superposition validator

    To create a superposition, a superlist is required.

    As an abstract superposition, the superlist is allowed
    to contain only one tuple and the interpretation of such
    case is depedent on the object.

    If the object type is not specified and is thus `None`,
    all components are required to be of the same type;
    otherwise (object type is provided) all components must
    be instances of that type.

    VALIDATED DATA

    Validated data is a dictionary that has one key `superlist`
    is the validated super list,
        `ret = {
                'superlist': self._validated_superlist
            }`
    """
    error_class = SuperpositionValidationError
    errro_location = _MODULE_LOCATION_ + '.SuperpositionValidator'

    def __init__(self, superlist=None, component_type=None):
        super().__init__()
        self._validated_superlist = None
        if not component_type is None:
            if isinstance(component_type, type):
                self._component_type = component_type
            else:
                self.report_errors('Component type given ' +\
                        'to specify the component of the ' +\
                        'superposition is neither valid '  +\
                        'nor a class.')
        else:
            self._component_type = None
        self.validate(superlist=superlist)
        if self.is_valid:
            self._validated_superlist = superlist

    def validate(self, superlist=None):
        """ Validate superlist

        Superlist is first validated by `SuperlistValidator`.

        Further requirements are observed.

        [1] If component type is not given, all components must
        be the same type.

        [2] If component type is given, all components must be
        or subclass of that type.
        """
        # 1. validate overal structure
        superlist_validator = SuperlistValidator(superlist=superlist)
        if not superlist_validator.is_valid:
            self.report_errors(superlist_validator.get_errors())
        # 2. Validate object type
        if len(self.get_errors()) == 0:
            for member in superlist:
                # if component type is None, components must
                # have the same type
                if self._component_type is None:
                    if not type(member[1]) is type(superlist[0][1]):
                        self.report_errors("Components in the " +\
                                "superlist do not have the same type.")
                # object type is given
                else:
                    if not isinstance(member[1], self._component_type):
                        self.report_errors("Components in "  +\
                                "the superlist do not have " +\
                                "the given object type.")

    def validated_data(self):
        ret = None
        if self.is_valid:
            ret = {
                'superlist': self._validated_superlist
            }
        return ret
