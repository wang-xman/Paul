# Quantum Gate
(Updated continuously)

Quantum gate package


## Design

A quantum gate is designed as a prototype class which is decorated by a 
decorator.


## Directory

* [base.py](./base.py) Base classes use throughout entire application
* [parameter.py](./parameter.py) Gate parameter objects
* [prototype](./prototype) Gate prototype subpack
  * [__init__.py](./prototype/__init__.py)
  * [errors.py](./prototype/errors.py)
  * [validators.py](./prototype/validators.py)
  * [base.py](./prototype/base.py)
* [enlarge_matrix](./enlarge_matrix) Matrix enlarge subpack
  * [errors.py](./enlarge_matrix/errors.py) Dedicated errors
  * [common.py](./enlarge_matrix/common.py)
  * [noncontrolled.py](./enlarge_matrix/noncontrolled.py)
  * [controlled_kernel.py](./enlarge_matrix/controlled_kernel.py)
  * [controlled_target_range.py](./enlarge_matrix/controlled_target_range.py)
  * [controlled_target_tuple.py](./enlarge_matrix/controlled_target_tuple.py)
  * [controlled.py](./enlarge_matrix/controlled.py)
* [decorator](./decorator) Gate decorator subpack
  * [noncontrolled.py](./decorator/noncontrolled.py) Noncontrolled mixin
  * [controlled.py](./decorator/controlled.py) Controlled operator mixin
  * [decorator.py](./decorator/decorator.py) Primary decorator
* [single_qubit.py](./single_qubit.py) Hardcoded single-qubit gate
* [multiple_qubit.py](./multiple_qubit.py) Hardcoded multiple-qubit gate