#!/bin/sh
echo "** Package-level Unit Test **"
echo ""
test_start=`date '+%Y_%m_%d__%H_%M_%S'`;

# Package: Common
./common/unittest/test.sh
echo ""

# Core Package: Linear Space
./linear_space/unittest/test.sh
echo ""

# Package: Bit
./bit/unittest/test.sh
echo ""

# Package: Superposition
./superposition/unittest/test.sh
echo ""

# Core Package: Quantum State
./quantum_state/unittest/test.sh
echo ""

# Core Package: Qubit
./qubit/unittest/test.sh
echo ""

# Package: Density Matrix
./density_matrix/unittest/test.sh
echo ""

# Package: Quantum Operator
./quantum_operator/unittest/test.sh
echo ""

# Core package: Gate
./gate/unittest/test.sh
echo ""

# Package: Measurement
./measurement/unittest/test.sh
echo ""

# TODO Package: Quantum algebra
./quantum_algebra/unittest/test.sh
echo ""

# Package: Quantum Register
./quantum_register/unittest/test.sh
echo ""

# Package: Quantum memory
./quantum_memory/unittest/test.sh
echo ""

# Package: Quantum instruction
./quantum_instruction/unittest/test.sh
echo ""

# Package: Quantum Operation
./quantum_operation/unittest/test.sh
echo ""

# Package: Quantum Flow
./quantum_flow/unittest/test.sh
echo ""

# Pacakge: Quantum Circuit
./quantum_circuit/unittest/test.sh
echo ""

test_end=`date '+%Y_%m_%d__%H_%M_%S'`;
echo "** Library-level Unit Test Summary **"
echo "** Test began at   $test_start   **";
echo "** Test ended at   $test_end   **";