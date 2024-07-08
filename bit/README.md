# Bit
(Updated continuously)

Bit package


## Design

Bit object package consists of mainly validators and
utility functions that validate and operate on bit
object, such as bitstring, bitlist, etc.

Wrapper classes such as `Bitstring` and `Bitlist` are
mainly for easy access to utitlity functions implemented
as methods. They are not core objects here.

## Directory

* [base.py](./base.py) Base classes used in package
* [errors.py](./errors.py) Dedicated errors
* [validators.py](./validator.py) Validators for bit object.
* [utils.py](./utils.py) Uility functions operating on bit object.
* [bitstring](./bitstring.py) Bitstring wrapper object
* [bitlist](./bitlist) Bitlist wrapper object
* [bitrange](./bitrange) Bitrange is widely used in down-stream packages