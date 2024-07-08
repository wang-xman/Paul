"""
PACKAGE

Bit

PATH

[app_root]/bit/

INTRO

Core items in this package are validators and utility
functions operating on bit objects.

Two wrapper classes `Bitstring` and `Bitlist` are designed
to integrate validation and for quick access to utility
functions.

LOG

Updated on 30 September 2021 | Created on 06 November 2020
"""
from .validators import BitstringValidator, BitarrayValidator, BitlistValidator
from .bitstring import Bitstring, Bitstring_Literal_Type
from .bitlist import Bitlist
from .bitrange import Bitrange
from .utils import bitarray_to_integer, bitstring_to_integer, \
    integer_to_bitstring, bitstring_to_fraction, bitstring_to_standard_basis, \
    integer_to_bitarray, bitlist_to_vector, vector_to_bitlist, flip_bit, \
    flip_all, swap_bits
