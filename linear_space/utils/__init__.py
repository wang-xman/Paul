"""
SUBPACK

Linear space utility functions subpack

PATH

[app_root]/linear_space/utils/

INTRO

Utility and helper functions.

"""
# utils imported from linear object subpack
from linear_space.linear_object.utils import is_scalar_like, is_column_like, \
    is_row_like, is_matrix_like, is_flat_list_like, is_empty, has_only_number, \
    has_only_integer, has_double_entry, maximum, minimum
from .makers import vector_from_list, vector_from_tuple, vector, \
    unitvector_from_list, unitvector_from_tuple, unitvector, \
    equally_weighted_vector, \
    matrix_from_array, matrix_from_list, matrix, \
    identity_by_rows, identity_by_bits, identity_one_bit
