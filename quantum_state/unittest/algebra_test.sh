#!/bin/sh

# Algebra module
echo "========================"
echo "| State Algebra Module |"
echo "========================"

echo "--- --- State scale --- ---"
python3 -m unittest quantum_state/unittest/algebra/test_state_scale.py

echo "--- --- State addition --- ---"
python3 -m unittest quantum_state/unittest/algebra/test_state_add.py

echo "--- --- State subtraction --- ---"
python3 -m unittest quantum_state/unittest/algebra/test_state_sub.py

echo "--- --- Inner product --- ---"
python3 -m unittest quantum_state/unittest/algebra/test_state_inner.py

echo "--- --- Outer product --- ---"
python3 -m unittest quantum_state/unittest/algebra/test_state_outer.py

echo "--- --- Kronecker product --- ---"
python3 -m unittest quantum_state/unittest/algebra/test_state_kronecker.py