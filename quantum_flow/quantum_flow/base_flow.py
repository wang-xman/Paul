

from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory, QubitRegisterMetadata
from quantum_operation.base_operation import BaseOperation
from .errors import BaseQuantumFlowError

_MODULE_LOCATION_ = 'quantum_flow.quantum_flow.base_flow'


class BaseQuantumFlow:
    """ Base quantum flow class

    Base flow class defines basic properties of flow object.

    Flow stores and manages a list of operation objects to be
    executed on a memory (or register). However, base flow
    class is storage agnostic, meaning it is insensitive to
    any feature of register or memory.

    One of the most important attributes of a flow object is
    the internal operation sequence `self._operation_sequence`
    which stores the list of operations executed sequentially.

    On the list, rank of an operation determines its position in
    the execution order, rank 0 is executed first, then rank 1,
    and so on.

    ATTRIBUTES

    `self.label` (`str`) : a string to identify a flow

    `self._operation_sequence` (`list`) : a list of operations
    to be executed; first (last) in the list is executed at
    the earliest (latest) moment

    `self.get_sequence()` : return the operation sequence, a list

    `self._append_to_sequence(,ops)` : append an operation or a
    list of operations to the operation sequence; NOTE Before
    calling this method, operations must be validated

    `self.is_valid_operation(,ops)` : verify if an operation or
    a list of operations is valid; returns `True` if valid,
    otherwise `False`
    """
    error_location = _MODULE_LOCATION_ + '.BaseQuantumFlow'

    def __init__(self, operation=None, label=None):
        """ Base Quantum Flow : Initialiser """
        self.label = label
        self._operation_sequence = []
        if self.is_valid_operation(operation):
            self._append_to_sequence(operation)
        else:
            raise BaseQuantumFlowError("To initialise a quantum flow, " +\
                    "one operation or a list of operations are required." +\
                    "Other objects are not accepted.")

    def _append_to_sequence(self, ops):
        """ Base Quantum Flow : Append operation to internal list

        If a list of operations is provided, the entire list is
        appended to the existing list, maitaining its order.

        This method is not intended to be used externally.
        Several public methods, having access to this method, are
        provided to user.
        """
        if isinstance(ops, list):
            self._operation_sequence.extend(ops)
        else:
            self._operation_sequence.append(ops)

    def is_valid_operation(self, ops):
        """ Base Quantum Flow : Verify an (list) operation """
        ret = False
        non_operation_counter = 0
        if isinstance(ops, list):
            for _ , op in enumerate(ops):
                if not isinstance(op, BaseOperation):
                    non_operation_counter += 1
        else:
            if not isinstance(ops, BaseOperation):
                non_operation_counter += 1
        if non_operation_counter == 0:
            ret = True
        return ret

    @property
    def is_empty(self):
        """ Base Quantum Flow : Return `True`/`False` if flow is/not empty """
        ret = True
        if len(self._operation_sequence) > 0:
            ret = False
        return ret

    @property
    def number_of_operations(self):
        """ Base Quantum Flow : Return number of operations in sequence """
        ret = len(self._operation_sequence)
        return ret

    def is_valid_rank(self, rank):
        """ Base Quantum Flow : Verify is an operation rank is valid """
        ret = False
        if rank in range(0, self.number_of_operations):
            ret = True
        return ret

    def get_sequence(self):
        """ Base Quantum Flow : Returns operation sequence """
        return self._operation_sequence

    def get_operation_by_rank(self, rank):
        """ Base Quantum Flow : Get operation at the given rank """
        ret = None
        if self.is_valid_rank(rank):
            ret = self._operation_sequence[rank]
        else:
            raise BaseQuantumFlowError("Rank to request operation " +\
                    "is invalid.")
        return ret

    def append(self, ops):
        """ Base Quantum Flow : Public append method

        Append one operation or a list of operations to the END of the
        operation sequence.

        Arguments

        `ops` (`Operation` or `list`): an operation object or a list of
        operation objects
        """
        if self.is_valid_operation(ops):
            self._append_to_sequence(ops)
        else:
            raise BaseQuantumFlowError("Quantum flow accepts only, " +\
                    "quantum operation or a list of them.",
                    location=self.error_location+'.append')

    def prepend(self, ops):
        """ Base Quantum Flow : Prepend an operation of a list operations

        Operation or the list of operations will be inserted at
        the HEAD of the sequence. (This is what prepend means.)

        In the case that `ops` is a list, the order of this list
        will remain.

        Arguments

        `ops` (`Operation` or `list`): an operation object or a list of
        operation objects
        """
        if self.is_valid_operation(ops):
            if isinstance(ops, list):
                self._operation_sequence[0:0] = ops
            else:
                self._operation_sequence.insert(0, ops)
        else:
            raise BaseQuantumFlowError("Operations to be " +\
                    "prepended to quantum flow are invalid.",
                    location=self.error_location+'.prepend')

    def insert(self, ops, rank=None):
        """ Base Quantum Flow : Insert an operation or a list of operation

        Insert the item at a given RANK. For example, if `rank` is 2,
        then the `ops` will be inserted into the sequence at the index
        2.

        Arguments

        `ops` (`Operation` or `list`): an operation object or a list of
        operation objects

        `rank` (`int`): intended rank of the operation (or list) in the
        sequence; NOTE If the intended rank is not given, the default
        action is to append to the END of the sequence
        """
        if self.is_valid_operation(ops):
            if rank is None:
                self.append(ops)
            elif rank in range(0, self.number_of_operations):
                if isinstance(ops, list):
                    self._operation_sequence[rank:rank] = ops
                else:
                    self._operation_sequence.insert(rank, ops)
            else:
                raise BaseQuantumFlowError("Rank of the operation " +\
                        "to be inserted is out of range.",
                        location=self.error_location+'.insert')
        else:
            raise BaseQuantumFlowError("Operations to be inserted " +\
                    "into quantum flow are invalid.",
                    location=self.error_location+'.insert')

    def merge(self, flowb):
        """ Base Quantum Flow : Merge two flows

        Operation sequence of `flowb` is merged into the current flow.
        Sequence of `flowb` is appended to the end of the current flow.

        TODO What happens to the labels? Default to the label of the
        first flow?

        Returns

        `self`: this flow object
        """
        if isinstance(flowb, BaseQuantumFlow):
            self.append(flowb.get_sequence())
        else:
            raise BaseQuantumFlowError("A flow object can only " +\
                    "merge with another flow object.",
                    location=self.error_location+'.merge')
        return self
