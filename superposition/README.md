# Superposition
(Updated continuously)

Superposition package


## Design

Superposition wraps a superlist. A superlist must
satisfy a set of criteria.

### Superlist

In a superlist, the algebraic relationship between any
two tuples is addition (+); within each tuple, the
relationship between two elements is multiplication.

### Superposition

Superposition is an abstract principle that governs
addition of objects.

Central to the principle is that summing up two
linearly scaled objects must yield an object the same
type. Here linearly scaled object means the object is
multiplied by a number.

Superposition principle is a reflection of properties
of vector. Quantum state is the most important example.
The superposition class implemented here emulates this
principle.

Abstract superposition principle applies to object of
any type. The underlying object must EITHER implement
multiplication (*), addition (+), and equal (==)
operators, OR have access to external methods that can
fulfill such operation. These operations are required
to convert a superposition into an object of the same
type.

In this application, the realisation of superposition
is via a list of tuples, referred to as 'superlist'.
Within the superlist, each tuple has exactly 2 elements.
First element is referred to as 'amplitude' and is often
a number. The second element is an instance of the
specified type and is often referred to as 'component'.
The tuple is sometimes referred to as 'member'.

In a superlist, the algebraic relationship between any
two tuples is addition (+); within each tuple, the
relationship between two elements is multiplication.


## Directory

* [base.py](./base.py) Base classes used in package
* [errors.py](./errors.py)
* [validators.py](./validators.py)
* [superlist.py](./superlist.py) Superlist validator
* [superposition.py](./superposition.py) Superposition class