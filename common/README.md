# Common

Application level common objects

## Log

Updated on 30 September 2021

## Directory

* [exception](./exception/) Exception subpack
  * [__init__.py]
  * [base.py]
  * [errors.py](./exception/errors.py) Base error class
  * [warning.py](./exception/warning.py) Base warning class
* [validator](./validator/) Validator subpack
  * [__init__.py]
  * [errors.py](./validator/errors.py) Error classes used by base validator
  * [base_validator.py](./validator/base_validator.py) Base validator class.
* [function](./function/) Function analyser and utility classes
  * [__init__.py]
  * [errors.py] Error classes
  * [validators.py] Validators
  * [utils.py] Utility functions
  * [decorators.py] Function decorators.
  * [signature.py] Signature analyzer
* [parameter](./parameter/) Parameter subpack
  * [__init__.py]
  * [errors.py] Errors for subpack
  * [validators.py] Valdiator for various types of parameters
  * [parameters.py] Collection of parameter classes.
* [string.py](./string.py) String related verifiers
* [mixins.py](./mixins.py) Mixin classes used in class design.