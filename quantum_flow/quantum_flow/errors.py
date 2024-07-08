from quantum_flow.base import QuantumFlowBaseError


class BaseQuantumFlowError(QuantumFlowBaseError):
    """ Error raised by base quantum flow
    ENTRY

    `base_flow.BaseQuantumFlow`
    """
    header = 'Base_Quantum_Flow_Error'


class QuantumFlowError(BaseQuantumFlowError):
    """ Error raised by quantum flow
    ENTRY

    `quantum_flow.BaseQuantumFlow`
    """
    header = 'Quantum_Flow_Error'
