#!/bin/sh

echo "********************"
echo "* Core Package     *"
echo "*     Linear Space *"
echo "********************"

# Number
./linear_space/unittest/number_test.sh

# Linear object
./linear_space/unittest/linear_object_test.sh

# Vector
./linear_space/unittest/vector_test.sh

# Matrix
./linear_space/unittest/matrix_test.sh

# Utils
./linear_space/unittest/utils_test.sh

# Algebra
./linear_space/unittest/algebra_test.sh

echo "**********************"
echo "**********************"