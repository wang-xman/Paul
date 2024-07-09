# Paul

```
The MIT License

Copyright © 2024 Matt Wang

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

Paul is a quantum computer simulator

## Design

General architecture of this application is called
VORE, for Validate-Object-and-Raise-Error.

Quantum computation simulator is designed around
three central objects, quantum state, quantum gate,
and quantum flow. Quantum flow is, at its core, a
series of operations on matrices.

This particular feature calls for a try-and-raise
type of approach: If a state vector is incompatible
with an operator, raise error; otherwise, apply.
Therefore, object involved in any such operation
shall be validated in advance, and errors are better
attached to the operation (function) that raises it.
In fact, this is what we do in linear algebra. For
example, should the dimensions of two matrices are
incompatible for matrix product, we raise error.

Validator is designed to track the locations an error
is reported or collected, which helps users to locate
the root of any error.

Errors are grouped according to 3 major categories, 
validation error, algebra error, and generic error.
Validation error is raised by a validator. Algebra
error is originated from an algebra function. Errors
raised elsewhere are considered generic.

## Features

Quantum state can be created via an intuitive *super list*
such as ```[(1.0, "000"), (1.0, "100"), (1.0, "010")]```
representing a superposition. Normalisation is quaranteed.
Linear algebraic operations are available for quantum states.

Dirac *ket* and *bra* are introduced as wrappers around
a quantum state and its hermitean conjugate.

Quantum gate can be described by a Python dictionary.
The key element here is a generic algorithm to construct a *multiple-controlled-multiple-qubit* gate, i.e. a gate
that operates on multiple qubits and requires multiple
bits as the control bits. In this regard, CNOT gate is
an edge case.

A *quantum flow* consists of a series of quantum gates.
It describes a sequence of applying quantum gates on
the state. Frequently used quantum operations, such as
Quantum Fourier Transformation, are modularised as a *quantum flow*.
User only needs to provide the indices (of the qubits) for such as transformation.

A *quantum circuit* is decomposed into a series of quantum
flows applying to a quantum state. 


## Update

Laste update 02 October 2021.

## Directory

Packages are listed according to the dependence hierarchy.
Most fundamental package is placed on the top.

### (Common)

* [common](./common) Package-level classes and routines for all packages.
  * [exception](./common/exception/) Exception subpack
    * [__init__.py](./common/exception/__init__.py)
    * [base.py](./common/exception/base.py)
    * [errors.py](./common/exception/errors.py) Base error class
    * [warning.py](./common/exception/warning.py) Base warning class
  * [validator](./common/validator/) Validator subpack
    * [__init__.py](./common/validator/__init__.py)
    * [errors.py](./common/validator/errors.py) Error classes used by base validator
    * [base_validator.py](./common/validator/base_validator.py) Base validator class.
  * [function](./common/function/) Function analyser and utility classes
    * [__init__.py](./common/function/__init__.py)
    * [errors.py](./common/function/errors.py) Error classes
    * [validators.py](./common/function/validators.py) Validators
    * [utils.py](./common/function/utils.py) Utility functions
    * [signature.py](./common/function/signature.py) Signature analyzer
    * [decorators.py](./common/function/decorators.py) Various function decorators.
  * [parameter](./common/parameter/) Parameter subpack
    * [__init__.py](./common/parameter/__init__.py)
    * [errors.py](./common/parameter/errors.py) Errors for subpack
    * [validators.py](./common/parameter/validators.py) Valdiator for various types of parameters
    * [parameters.py](./common/parameter/parameters.py) Collection of parameter classes.
  * [string.py](./common/string.py) String related verifiers
  * [mixins.py](./common/mixins.py) Mixin classes used in class design.

### (Foundation)

* [linear_space](./linear_space) Linear space package
  * [base.py](./linear_space/base.py) Base classes used in package
  * [numpy_lib](./linear_space/numpy_lib.py) Numpy functions and classes. 
  * [number](./linear_space/number) Number subpack
    * [__init__.py](./linear_space/number/__init__.py)
    * [errors.py](./linear_space/number/errors.py) Error classes
    * [types.py](./linear_space/number/types.py) Number types used only for isinstance
    * [utils.py](./linear_space/number/utils.py) Verifiers and utility functions.
  * [linear_object](./linear_space/linear_object) Linear object subpack
    * [__init__.py](./linear_space/linear_object/__init__.py)
    * [errors.py](./linear_space/linear_object/errors.py) Errors.
    * [validators.py](./linear_space/linear_object/validators.py) Validators.
    * [linear_object.py](./linear_space/linear_object/linear_object.py) Linear obejct.
    * [utils.py](./linear_space/linear_object/verifier.py) Verification functions.
    * [types.py](./linear_space/linear_object/types.py) Linear object subtypes.
    * [decorator.py](./linear_space/linear_object/decorator.py) Decorator for algebra functions.
    * [algebra.py](./linear_space/linear_object/algebra.py) Linear algebra functions
  * [vector](./linear_space/vector) Vector subpack
    * [__init__.py](./linear_space/vector/__init__.py)
    * [base.py] Base classes and third party packages
    * [errors.py](./linear_space/vector/errors.py) Errors
    * [validators.py](/linear_space/vector/validators.py) Validators
    * [base_vector.py](./linear_space/vector/base_vector.py) Base vector.
    * [column_vector.py](./linear_space/vector/column_vector.py) Column vector
    * [unit_vector.py](./linear_space/vector/unit_vector.py) Unit (column) vector
    * [standard_basis.py](./linear_space/vector/standard_basis.py) Standard basis vector
    * [row_vector.py](./linear_space/vector/row_vector.py) Row vector
  * [matrix](./linear_space/matrix) Matrix subpack
    * [__init__.py](./linear_space/matrix/__init__.py)
    * [errors.py](./linear_space/matrix/errors.py)
    * [validators.py](./linear_space/matrix/validators.py)
    * [matrix.py](./linear_space/matrix/matrix.py) Generic matrix object.
    * [square_matrix.py](./linear_space/matrix/square_matrix.py) Square matrix class
    * [identity_matrix.py](./linear_space/matrix/identity_matrix.py) Identity matrix class
    * [special.py](./linear_space/matrix/special.py) Special matrices objects
  * [utils](./linear_space/utils) Utility functions subpack
    * [__init__.py](./linear_space/utils/__init__.py)
    * [errors.py](./linear_space/utils/errors.py) Errors for subpack
    * [makers.py](./linear_space/utils/makers.py) Object makers
  * [algebra](./linear_space/algebra) Package-level algebra functions
    * [__init__.py](./linear_space/algebra/__init__.py)
    * [errors.py](./linear_space/algebra/errors.py) Error class for algebra functions (LSAFE).
    * [decorator.py](./linear_space/algebra/decorator.py) Algebra function decorator
    * [functions.py](./linear_space/algebra/functions.py) Algebra functions - LSAF

* [bit](./bit) Bit package
  * [base.py](./bit/base.py) Base classes used in package
  * [errors.py](./bit/errors.py)
  * [validators.py](./bit/validator.py) Validators for bit object.
  * [utils.py](./bit/utils.py) Uility functions operating on bit object.
  * [bitstring](./bit/bitstring.py) Bitstring wrapper object
  * [bitlist](./bit/bitlist) Bitlist wrapper object
  * [bitrange](./bit/bitrange) Bitrange wrapper object

### (Kernel)
* [superposition](./superposition) Superposition package
  * [base.py](./superposition/base.py) Base classes used in package
  * [errors.py](./superposition/errors.py)
  * [validators.py](./superposition/validators.py)
  * [superlist.py](./superposition/superlist.py) Superlist validator
  * [superposition.py](./superposition/superposition.py) Superposition class

* [quantum_state](./quantum_state) Quantum state (core) package.
  * [base.py](./quantum_state/base.py) Base exception and validators for package.
  * [errors.py](./quantum_state/errors.py) Dedicated errors
  * [validators.py](./quantum_state/validators.py) Validators.
  * [null_state.py](./quantum_state/null_state.py) Null state singleton.
  * [quantum_state.py](./quantum_state/quantum_state.py) Generic quantum state class
  * [superposition.py](./quantum_state/superposition.py) Quantum superposition class.
  * [braket.py](./quantum_state/braket.py) Dirac braket wrapper object.
  * [utils.py](./quantum_state/utils.py) Utility functions
  * [algebra](./quantum_state/algebra) Quantum state algebra subpack
    * [__init__.py](./quantum_state/algebra/__init__.py)
    * [errors.py](./quantum_state/algebra/errors.py) Quantum state algebra function errors
    * [decorator.py](./quantum_state/algebra/decorator.py) Algebra function decorator
    * [functions.py](./quantum_state/algebra/functions.py) Quantum algebra for state and superposition.

* [qubit](./qubit) Qubit package
  * [base.py](./qubit/base.py) Package-wide base classes
  * [errors.py](./qubit/errors.py) Dedicated errors
  * [validators.py](./qubit/validator.py) Validators.
  * [qubit.py](./qubit/qubit.py) Qubit state and its derivatives.
  * [special.py](./qubit/special.py) Special qubit states.
  * [index_range.py](./qubit/index_range.py) Index range related classes.
  * [utils.py](./qubit/utils.py) Makers and verifiers.
  * [algebra.py](./qubit/algebra.py) Quantum algebra for qubits and superposition

* [density_matrix](./density_matrix) Density matrix package
  * [base.py](./density_matrix/base.py) Base classes used in package
  * [errors.py](./density_matrix/errors.py)
  * [validators.py](./density_matrix/validators.py) Validators used for initialisation.
  * [density_matrix.py](./density_matrix/density_matrix.py) Density matrix object.
  * [utils.py](./density_matrix/utils.py)

* [quantum_operator](./quantum_operator) Quantum operator package
  * [errors](./quantum_operator/errors/py)
  * [parameter](./quantum_operator/parameter.py) Quantum operator parameters
  * [quantum_operators](./quantum_operator/quantum_operators.py) Generic
  quantum operator objects

* [gate](./gate) Quantum gate package. See README.md[](./gate/README.md)
  * [base.py](./base.py) Base classes use throughout entire application
  * [parameter.py](./parameter.py) Gate parameter objects
  * [prototype](./prototype) Gate prototype subpack
    * [base.py](./prototype/base.py)
    * [errors.py](./prototype/errors.py)
    * [validators.py](./prototype/validators.py)
  * [enlarge_matrix](./enlarge_matrix) Matrix enlarge subpack
    * [errors.py]
    * [common.py](./enlarge_matrix/common.py)
    * [noncontrolled.py](./enlarge_matrix/noncontrolled.py)
    * [controlled_kernel.py](./enlarge_matrix/controlled_kernel.py)
    * [controlled_target_range.py](./enlarge_matrix/controlled_target_range.py)
    * [controlled_target_index.py](./enlarge_matrix/controlled_target_index.py)
    * [controlled.py](./enlarge_matrix/controlled.py)
  * [decorator](./decorator) Gate decorator subpack
    * [noncontrolled.py](./decorator/noncontrolled.py) Noncontrolled operator
      mixin class
    * [controlled.py](./decorator/controlled.py) Controlled operator mixin class
    * [decorator.py](./decorator/decorator.py) Primary decorator
  * [single_qubit.py](./single_qubit.py) Hardcoded single-qubit gate
  * [multiple_qubit.py](./multiple_qubit.py) Hardcoded multiple-qubit gate

* [measurement](./measurement) Quantum measurement package
  * [__init__.py](./measurement/__init__.py)
  * [base.py](./measurement/base.py) Base error and validator.
  * [errors.py](./measurement/errors.py) Dedicated errors
  * [validators.](./measurement/validators.py) Validators
  * [partial_trace.py](./measurement/partial_trace.py) Partial trace functions
  * [projective.py](./measurement/projective.py) Porjective measurement functions.

* [quantum_algebra](./quantum_algebra/) TODO

### (Storage)

* [quantum_register](./quantum_register) Quantum register package
  * [base.py](./quantum_register/base.py) Base classes for package
  * [errors.py](/quantum_register/errors.py)
  * [validators.py](/quantum_register/validators.py)
  * [base_register.py](/quantum_register/base_register.py)
  * [registers.py](./quantum_register/registers.py) Different types of registers

* [quantum_memory](./quantum_memory) Quantum memory package
  * [base.py](./quantum_memory/base.py) Base classes for package
  * [errors.py]
  * [validators.py](./quantum_memory/validator.py) Validator classes
  * [metadata.py](./quantum_memory/metadata.py) Metadata object
  * [managers.py](./quantum_memory/manager.py) Manager mixin classes for memory
  * [base_memory.py](./quantum_memory/base_memory.py) Base memory
  * [qubit_memory.py](./quantum_memory/qubit_memory.py) Qubit memory

### (Interface)

* [quantum_instruction](./quantum_instruction) Quantum instruction package
  * [base.py](./quantum_instruction/base.py) Base classes for package
  * [errors.py](./quantum_instruction/errors.py)
  * [validators.py](./quantum_instruction/validators.py) Dedicated validators
  * [gate](./quantum_instruction/gate) Gate operation instruction subpack
    * [__init__.py]
    * [errors.py](./quantum_instruction/gate/errors.py) Dedicated errors
    * [validators.py](./quantum_instruction/gate/validators.py)
    * [instructions.py](./quantum_instruction/gate/instructions.py)
  * [partial_trace](./quantum_instruction/partial_trace/) Partial trace instruction.
    * [__init__.py](./quantum_instruction/partial_trace/__init__.py)
    * [errors.py](./quantum_instruction/partial_trace/errors.py)
    * [validators.py](./quantum_instruction/partial_trace/validators.py)
    * [instructions.py](./quantum_instruction/partial_trace/instructions.py)
  * [measurement](./quantum_instruction/measurement/) Measurement instruction.
    * [__init__.py](./quantum_instruction/measurement/__init__.py)
    * [errors.py](./quantum_instruction/measurement/errors.py)
    * [validators.py](./quantum_instruction/measurement/validators.py)
    * [instructions.py](./quantum_instruction/measurement/instructions.py)
  Quantum instruction for measurement operation.

### (Dynamics)

* [quantum_operation](./quantum_operation) Quantum Operation package
  * [base.py]
  * [base_operation](./quantum_operation/base_operation/) Base classes for package
    * [errors.py](./quantum_operation/base_operation/errors.py)
    * [validators.py](./quantum_operation/base_operation/validators.py)
    * [operations.py](./quantum_operation/base_operation/operations.py)
  * [gate](./quantum_operation/gate_operation/) Gate operation subpack
    * [errors.py]
    * [validators.py]
    * [operations.py]
    * [utils]
  * [partial](./quantum_operation/partial_trace/) Partial trace operation subpack
    * [errors.py]
    * [validators.py]
    * [operations.py]
    * [utils]
  * [measurement](./quantum_operation/measurement/) Measurement operation subpack
    * [errors.py]
    * [validators.py]
    * [operations.py]
    * [utils]
  
* [quantum_flow](./quantum_flow) Quantum Flow package
  * [base.py]
  * [quantum_flow](./quantum_flow/quantum_flow/)
    * [errors.py]
    * [validators]
    * [base_flow.py](./quantum_flow/base.py) Base classes for package
    * [quantum_flow.py](./quantum_flow/quantum_flow.py) Quantum flow
    * [utils.py]
  * [makers](./quantum_flow/makers/)
    * [walsh_hadamard.py](./quantum_flow/makers/walsh_hadamard.py) Walsh-Hadamard
    * [swap.py](./quantum_flow/makers/swap.py) SWAP related flows
    * [fourier.py](./quantum_flow/makers/fourier.py) Quantum Fourier flow
    * [reflection.py](./quantum_flow/makers/reflection.py) Reflection flow

* [quantum_circuit](./quantum_circuit) Quantum circuit package
  * [base.py](./quantum_circuit/base.py) Base classes to package
  * [grover.py](./quantum_circuit/grover.py) Grover circuit
  * [phase_estimation.py](./quantum_circuit/phase_estimation.py) Phase estimation circuit
  * [amplitude_estimation.py](./quantum_circuit/amplitude_estimation.py)
