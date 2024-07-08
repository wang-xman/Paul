#!/bin/sh

echo "***************"
echo "* Package     *"
echo "*     Qubit   *"
echo "***************"

# Validators
./qubit/unittest/validators_test.sh

# Qubit 
./qubit/unittest/qubit_test.sh

# Special states
./qubit/unittest/special_state_test.sh

# Index range
./qubit/unittest/index_range_test.sh

# Utils
./qubit/unittest/utils_test.sh

# Algebra
./qubit/unittest/algebra_test.sh

echo "***************"
echo "***************"