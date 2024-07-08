#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
PACKAGE

Linear space

PATH

[app_root]/linear_space/

INTRO

Linear space package defines 4 core objects: linear object,
scalar, vector and matrix. The last three objects are all
derived from linear object. Linear space is the most basic
mathematical concept behind quantum mechanics.

All linear objects are separated from algebra operations.
Algebraic operations are not implemented as methods of
linear objects but standalone algebra functions. In this
design, algebra functions overseas all available objects
and can better decide on the result of the operation.

Linear object package is designed towards an standalone
package on which a full application can be developed.

TODO

[2] Should I introduce a scalar subpack?

[3] Eigensystem or related operations?

[4] In matrix.matrix, implement string representation
for generic matrix.

LOG

Updated on 27 September 2021 | Created on 14 April 2021
"""
