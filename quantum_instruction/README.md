# Quantum instruction

## Directory

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