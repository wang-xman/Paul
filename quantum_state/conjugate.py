"""
MODULE

quantum_state.conjugate.py

PATH

[app_root]/quantum_state/conjugate.py

INTRO

Quantum state conjugate object.

Quantum state conjugate is not a quantum state. It is
a linear transformation of quantum state.

CONTENT

`QuantumStateConjugate` - Quantum state conjugate

TODO Not unittested

LOG

Updated on 29 September 2021 | Created on 27 September 2021
"""
from linear_space.algebra import hermitian_conjugate
from .errors import QuantumStateConjugateError
from .quantum_state import QuantumState

_MODULE_LOCATION_ = 'quantum_state.conjugate'


class QuantumStateConjugate:
    """ Quantum state conjugate

    Quantum state conjugate is NOT a state, but a linear
    transformation of it. In terms of Dirac braket, it
    is a bra, a quantum state is a ket.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.QuantumStateConjugate'

    def __init__(self, state=None):
        if isinstance(state, QuantumState):
            self._state = state
        else:
            raise QuantumStateConjugateError("A quantum state is required " +\
                    "to create a state conjugate",
                    location=self._ERROR_LOCATION_+'.__init__')

    def as_vector(self):
        """ Quantum State Conjugate :: Return a row vector

        Vector of a state conjugate is a row vector converted
        from state vector via hermitian conjugate.
        """
        return hermitian_conjugate(self._state.as_vector())

    @property
    def vector(self):
        """ Quantum State Conjugate :: Alias to `as_vector()` """
        return self.as_vector()

    def as_array(self):
        """ Quantum State Conjugate :: Return internal vector as array """
        return self.as_vector().as_array()

    @property
    def size(self):
        """ Quantum State Conjugate :: size of state vector """
        return self.as_vector().size

    def dimension(self):
        """ Quantum State Conjugate :: Number of elements

        Returns the Number of elements in internal vector
        `self._vector`.
        """
        return self.as_vector().size
