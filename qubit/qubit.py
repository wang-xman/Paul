#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.qubit.py

PATH

[app_root]/qubit/qubit.py

INTRO

Qubit state object.

Qubit state and computational basis state are quantum
states designed for qubit-based systems. Computational
basis state, aka computational basis, is a specialised
qubit state.

Important concepts

basislist: similar to bitlist but with bitstring replaced
by the cooresponding computational basis state. A basislist
is a superlist by using computational basis state as component
object.

CONTENT

`QubitState` - Base class to all qubit states.

`ComputationalBasis` - Computational basis

`SingleQubitBasis` - Single qubit computational basis

`QubitSuperposition` - Qubit superposition object

LOG

Updated on 30 September 2021 | Created on 13 November 2020
"""
from linear_space.number import is_zero, exponent_of_two
from bit import BitstringValidator, Bitstring
from bit.utils import vector_to_bitlist, integer_to_bitstring
from quantum_state import QuantumState, Ket, Bra, QuantumSuperposition
from quantum_state.utils import is_spinup, is_spindown

from .errors import QubitStateError
from .validators import QubitStateValidator, SingleQubitBasisValidator

_MODULE_LOCATION_ = 'qubit.qubit'


class QubitState(QuantumState):
    """ Qubit state

    Qubit state is a quantum state.

    It combines linearly computational basis states.
    To represent a superposition, in parallel to its
    intrinsic property as a vector, a qubit state is
    can be denoted as a list of amplitude-basis (state)
    tuples. Since qubit state is a quantum state, its
    instantiation is still via a vector.

    In addition, a utility function - not part of this
    class - is provided to create a qubit state instance
    by using a bitlist. An example of a bitlist is
        [(0.5, '00'), (0.5, '01'), (0.5, '10')],
    which is a modified version of superlist in which
    component object is replaced by a bitstring.

    CONSTRUCTOR

    `__init__(, vector, state)`: either a vector or quantum
    state instance is provided to instantiate a qubit state

    ATTRIBUTES

    [Basic]

    `self.number_of_qubits`: property; returns the number of
    qubits calculated from the internal vector

    `self.noq`: property; alias to `self.number_of_qubits`

    `self.is_valid_qubit_index(, qindex)`: validate an index
    used to reference one qubit in the state

    `self.as_bitlist()`: returns a bitlist by invoking the
    `vector_to_bitlist` helper function

    `self.as_basislist()`: returns a list of tuples each
    contains an amplitude and a computational basis state

    `self.as_superposition()`: returns the qubit state as a
    superposition of the computational basis states;
    a superposition object.

    [Logic]

    `self.is_up`: property; returns `True` (`False`) if state
    is/not spin-up; to be a spin-up state also means a
    single-qubit state

    `self.is_down`: property; returns `True` (`False`) if
    state is/not spin-down

    [Presentation]

    `ket_prepresentation()`: return a string that represents
    the linear superposition of the kets.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.QubitState'

    def __init__(self, vector=None, state=None):
        """ Qubit State :: init

        Validate the size of the vector to make sure
        it is compatible with qubit.
        """
        validator = QubitStateValidator(vector=vector, state=state)
        if validator.is_valid:
            validated_vector = validator.validated_data()['vector']
            try:
                super().__init__(vector=validated_vector)
            except Exception as e:
                raise QubitStateError(str(e),
                        location=self._ERROR_LOCATION_+'.__init__')
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')

    @property
    def number_of_qubits(self):
        """ Qubit State :: Number of qubits

        Number of qubits is implied from the qubit state vector
        """
        noq = exponent_of_two(self._vector.size)
        return noq

    @property
    def noq(self):
        """ Qubit State :: Number of qubits """
        return self.number_of_qubits

    def is_valid_qubit_index(self, qindex):
        """ Qubit State :: Verify qubit-index

        Return `True` (`False`) if an index is valid (invalid).

        Index must be scientific index starting from 0.
        For example, if there are 10 qubits in the state,
        the valid range of qubit-index is [0, 9].

        NOTE Qubit-index is conceptually different from the
        index used to reference component in state vector.
        """
        ret = False
        if qindex in range(0, self.noq, 1):
            ret = True
        return ret

    def as_bitlist(self):
        """ Qubit State :: Returns a bitlist

        An example of bit list is
            [(0.5, '00'), (0.5, '11'), ...],
        second object in a tuple is a bitstring.

        NOTE Zero amplitude removal is performed in
        `vector_to_bitlist` function.
        """
        bitlist = vector_to_bitlist(self._vector)
        return bitlist

    def as_basislist(self):
        """ Qubit State :: Returns a basislist

        An example of basislist is
            [(0.5, Basis('00')), (0.5, Basis('11'))].
        Compared with bitlist, basislist contains `Basis`
        instance instead of its bitstring.

        A basis list can be used a superlist to instantiate
        a superposition.
        """
        basislist = []
        # calculate number of qubits
        noq = exponent_of_two(self._vector.size)
        for idx, amp in enumerate(self._vector.as_array()):
            if not is_zero(amp[0]):
                # convert an integer to binary string
                bitstring = integer_to_bitstring(integer=idx, total_digits=noq)
                basislist.append(
                        (amp[0], ComputationalBasis(bitstring=bitstring),))
        return basislist

    def as_superposition(self):
        """ Qubit State :: Return a superposition

        Returned superposition has computational basis
        as component.
        """
        superposition = QubitSuperposition(superlist=self.as_basislist())
        return superposition

    @property
    def is_up(self):
        """ Qubit State: Check if a spin-up (0) state """
        return is_spinup(self)

    @property
    def is_down(self):
        """ Qubit State: Check if a spin-down (1) state """
        return is_spindown(self)

    def ket_representation(self):
        """ State as a superposition of basis kets

        Returns a string of ket representation.

        In general a qubit state is a linear superposition,
        it can be represented as, for example,
            `0.5 |00> + 0.5 |01> + 0.5 |10> + 0.5 |11>`,
        which is ket representation refers to.

        TODO Format complex and float.
        """
        string = ""
        for i, item in enumerate(self.as_bitlist()):
            ks = str(item[0]) + "|"+ str(item[1]) + ">"
            string += ks
            if i < len(self.as_bitlist()) - 1:
                string += " + "
        return string


class ComputationalBasis(QubitState):
    """ Computational basis state

    Computational basis state (or simply basis) is
    a specialised qubit state, ergo a subaclass to
    `QubitState`, that has only one amplitude-basis
    tuple with an amplitude 1.

    Its internal vector is therefore a standard basis
    vector. The label of a basis state ket is the
    bitstring that, conforming to the given number of
    qubits, represents the standard basis vector.

    To instantiate a basis, use a bitstring that
    represents a qubit basis state, such as '000' for |000>.

    CONSTRUCTOR

    `bitstring` (`str`): a string variable of only 0 and
    1 that is used to designate a computational basis state.

    ATTRIBUTES

    [Basic]

    `self._bitstring_object` (`Bitstring`) : a `Bitstring`
    object converted from the bitstring; use of bitstring
    object instead of string simplifies conversion

    `self.__update_internal_vector()`: updates internal vector
    whenever the internal binary is modified

    `self.as_bitstring()`: returns bitstring of basis state

    `self.bitstring`: property; alias to `self.as_bitstring()`;
    newly added

    `self.as_list()`: returns a list of 0 and 1, all integers

    `self.as_tuple()`: returns a tuple of 0 and 1, all integers

    `self.decompose()`: returns a tuple of `SingleQubitBasis`
    instances; this basis state is seen as a tensor product of
    single basis states in this tuple

    [Logic]

    Falls back to `QuantumState`

    [Bitwise]

    `self.get_state_at(, index)`: returns a single qubit basis
    given by `index`

    `self.at(, index)`: alias to `self.get_state_at()`

    [Presentation]

    `self.as_ket()`: returns a `Ket` instance that has `_bitstring`
    as the label

    `self.ket_representation()`: returns a string that represents
    the state as, for example, a ket '|010>'
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.ComputationalBasis'

    def __init__(self, bitstring=None):
        """ Comp Basis :: init

        Computational basis state is a subclass of
        `BaseQubitState` with a vector that has only
        one nonzero component and that component is 1.
        """
        validator = BitstringValidator(bitstring=bitstring)
        if validator.is_valid:
            vd = validator.validated_data()
            self._bitstring_object = Bitstring(bitstring=vd['bitstring'])
            self._vector = None
            super().__init__(vector=self._bitstring_object.as_standard_basis())
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')

    def __update_internal_vector(self):
        """ Comp Basis :: Private method

        Whenever attribute `_bitstring` is modified, the
        internal vector must be updated accordingly.
        """
        self._vector = self._bitstring_object.as_standard_basis()

    def as_bitstring(self):
        """ Comp Basis :: Returns bitstring as string """
        return self._bitstring_object.as_string()

    @property
    def bitstring(self):
        """ Comp Basis :: Alias to as_bitstring """
        return self.as_bitstring()

    def as_list(self):
        """ Comp Basis :: Return a list of 0 and 1 (integers) """
        return self._bitstring_object.as_list()

    def as_tuple(self):
        """ Comp Basis :: Convert a tuple of 0 and 1 (integers) """
        return self._bitstring_object.as_tuple()

    def decompose(self):
        """ Comp Basis :: Decompose into single-qubit basis

        Returns a tuple of single qubit basis states.
        """
        tup = tuple()
        for bitchar in self.as_bitstring():
            tup += (SingleQubitBasis(bitstring=bitchar),)
        return tup

    def __getitem__(self, qindex):
        """ Comp Basis :: Operator [qindex]

        Return single qubit basis at given index.
        Index must be in scientific indexing scheme.

        NOTE Overrides the same method of a generic
        quantum state. In generic `QuantumState` this method
        returns the indexed element of the internal vector.
        """
        ret = None
        if self.is_valid_qubit_index(qindex):
            ret = self.decompose()[qindex]
        else:
            raise QubitStateError("Index in a computational " +\
                    "basis is out of range.",
                    location=self._ERROR_LOCATION_+'.__getitem__')
        return ret

    def get_state_at(self, qindex):
        """ Comp Basis :: Alias to `__getitem__()` method """
        return self.__getitem__(qindex)

    def at(self, qindex):
        """ Comp Basis :: Alias to `__getitem__()` method """
        return self.__getitem__(qindex)

    def as_ket(self):
        """ Comp Basis :: Returns a ket

        This state is held as the quantum state for a ket.
        Binary string is used as the ket string.
        """
        return Ket(label=self.as_bitstring(), state=self)

    def as_bra(self):
        """ Comp Basis :: convert to bra """
        return Bra(label=self.as_bitstring(), state=self)

    def ket_representation(self):
        """ Comp Basis :: Return |[ket_string]> string """
        return self.as_ket().representation()


class SingleQubitBasis(ComputationalBasis):
    """ Single qubit computational basis

    Basis state for a single qubit is either |0> for spin up,
    or |1> for spin down.

    To instantiate this class, only char '0' or '1' is allowed.

    CONSTRUCTOR

    `bitstring` (`str`): only '0' or '1' is acceptable.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.SingleQubitState'

    def __init__(self, bitstring=None):
        validator = SingleQubitBasisValidator(bitstring=bitstring)
        if validator.is_valid:
            vd = validator.validated_data()
            super().__init__(bitstring=vd['bitstring'])
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__int__')

    def __repr__(self):
        return self.ket_representation()

    def __str__(self):
        return self.ket_representation()


class QubitSuperposition(QuantumSuperposition):
    """ Superposition of qubit states """
    component_type = QubitState

    @property
    def number_of_qubits(self):
        return self.as_superlist()[0][1].number_of_qubits

    @property
    def noq(self):
        return self.number_of_qubits
