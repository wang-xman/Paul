#!/bin/sh

echo "*********************"
echo "* Package           *"
echo "*     Quantum State *"
echo "*********************"

# Quantum state validator
./quantum_state/unittest/validator_test.sh

# Null state
./quantum_state/unittest/null_state_test.sh

# Quantum state
./quantum_state/unittest/quantum_state_test.sh

# Superposition
./quantum_state/unittest/superposition_test.sh

# Algebra
./quantum_state/unittest/algebra_test.sh

# Braket
./quantum_state/unittest/braket_test.sh

echo "*********************"
echo "*********************"