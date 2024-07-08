#!/bin/sh

echo "========================"
echo "| Qubit Algebra Module |"
echo "========================"

# Scale
echo "--- --- Scale function --- ---"
python3 -m unittest qubit/unittest/algebra/test_qubit_scale.py

# Add
echo "--- --- Addition --- ---"
python3 -m unittest qubit/unittest/algebra/test_qubit_add.py

# Sub
echo "--- --- Subtraction --- ---"
python3 -m unittest qubit/unittest/algebra/test_qubit_sub.py

# Inner
echo "--- --- Inner product --- ---"
python3 -m unittest qubit/unittest/algebra/test_qubit_inner.py

# Outer
echo "--- --- Outer product --- ---"
python3 -m unittest qubit/unittest/algebra/test_qubit_outer.py

# Kronecker
echo "--- --- Kronecker product --- ---"
python3 -m unittest qubit/unittest/algebra/test_qubit_kronecker.py