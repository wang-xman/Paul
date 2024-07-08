#!/bin/sh
echo "********************"
echo "* Package          *"
echo "*     Quantum Gate *"
echo "********************"

# Parameter
./gate/unittest/test_shell/parameter_test.sh

# Base Prototypes
./gate/unittest/test_shell/prototype_base_test.sh

# Enlarge matrix routines
./gate/unittest/test_shell/enlarge_matrix_test.sh

# Decorator
./gate/unittest/test_shell/decorator_test.sh

# Single-qubit gates
./gate/unittest/test_shell/single_gate_module_test.sh

# Multiple-qubit gates
./gate/unittest/test_shell/multiple_qubit_gate_module_test.sh

# Controlled gate operations
./gate/unittest/test_shell/controlled_multiple_test.sh
#FIRST # end block comment

echo "**********************"
echo "**********************"