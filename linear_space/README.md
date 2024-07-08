# Linear Space
(Updated continuously)

Linear space package

TODO Should I introduce a scalar subpack

## Design

Central to linear space package is linear object
which is constructed in linear object subpack.
Linear object lays out the blueprint for derived
objects such as vector and matrix.

Linear object and its derivatives are separated
from algebra functions that operate on them.


## Directory

* [base.py](./base.py) Base classes used in package
* [numpy_lib](./numpy_lib.py) Numpy functions and classes. 
* [number](./number) Number subpack
  * [__init__.py](./number/__init__.py)
  * [errors.py](./number/errors.py) Error classes
  * [types.py](./number/types.py) Number types used only for isinstance
  * [utils.py](./number/utils.py) Verifiers and utility functions.
* [linear_object](./linear_object) Linear object subpack
  * [__init__.py](./linear_object/__init__.py)
  * [errors.py](./linear_object/errors.py) Errors.
  * [validators.py](./linear_object/validators.py) Validators.
  * [linear_object.py](./linear_object/linear_object.py) Linear obejct.
  * [utils.py](./linear_object/verifier.py) Verification functions.
  * [types.py](./linear_object/types.py) Linear object subtypes.
  * [decorator.py](./linear_object/decorator.py) Decorator for algebra functions.
  * [algebra.py](./linear_object/algebra.py) Linear algebra functions
* [vector](./vector) Vector subpack
  * [__init__.py](./vector/__init__.py)
  * [base.py] Base classes and third party packages
  * [errors.py](./vector/errors.py) Errors
  * [validators.py](/vector/validators.py) Validators
  * [base_vector.py](./vector/base_vector.py) Base vector.
  * [column_vector.py](./vector/column_vector.py) Column vector
  * [unit_vector.py](./vector/unit_vector.py) Unit (column) vector
  * [standard_basis.py](./vector/standard_basis.py) Standard basis vector
  * [row_vector.py](./vector/row_vector.py) Row vector
* [matrix](./matrix) Matrix subpack
  * [__init__.py](./matrix/__init__.py)
  * [errors.py](./matrix/errors.py)
  * [validators.py](./matrix/validators.py)
  * [matrix.py](./matrix/matrix.py) Generic matrix object.
  * [square_matrix.py](./matrix/square_matrix.py) Square matrix class
  * [identity_matrix.py](./matrix/identity_matrix.py) Identity matrix class
  * [special.py](./matrix/special.py) Special matrices objects
* [utils](./utils) Utility functions subpack
  * [__init__.py]
  * [errors.py](./utils/errors.py) Errors for subpack
  * [makers.py](./utils/makers.py) Object makers
* [algebra](./algebra) Package-level algebra functions
  * [__init__.py](./algebra/__init__.py)
  * [error.py](./algebra/error.py) Error class for algebra functions (LSAFE).
  * [decorator.py](./algebra/decorator.py) Algebra function decorator
  * [functions.py](./algebra/functions.py) Algebra functions - LSAF