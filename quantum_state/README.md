# Quantum state package

Quantum state package is a core package that powers
the entire application by providing the most important
object, quantum state, and the associated algebraic
methods.

## Log

Updated on 25 September 2021

## Null state

## Quantum state

Class ``QuantumState`` models the generic behaviour of 
quantum state. At its core, it is represented by an 
internal vector array to highlight the property of linear 
superposition.

## Quantum superposition

## Dirac braket

## Quantum state algebra

## Directory

* [base.py](./base.py) Abstract classes, base exception and 
  validators for package.
* [errors.py](./errors.py) 
* [validators.py](./validator.py) Validators.
* [null_state.py](./null_state.py) Null state singleton.
* [quantum_state.py](./quantum_state.py) Quantum state class
* [conjugate.py](./conjugate.py) Quantum state conjugate
* [superposition.py](./superposition.py) Quantum superposition class.
* [braket.py](./braket.py) Dirac braket wrapper object.
* [utils.py](./utils.py) Utility functions
* [algebra](./algebra) Quantum state algebra subpack
  * [__init__.py](./algebra/__init__.py)
  * [errors.py](./algebra/errors.py) Quantum state algebra function errors
  * [decorator.py](./algebra/decorator.py) Algebra function decorator
  * [functions.py](./algebra/functions.py) Quantum algebra for state and superposition.