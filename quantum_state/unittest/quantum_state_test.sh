#!/bin/sh

# Quantum state module
echo "========================"
echo "| Quantum State Module |"
echo "========================"

echo "--- --- Init --- ---"
python3 -m unittest quantum_state/unittest/quantum_state/test_init.py

echo "--- --- Indexing --- ---"
python3 -m unittest quantum_state/unittest/quantum_state/test_indexing.py

echo "--- --- Vector type and dimension --- ---"
python3 -m unittest quantum_state/unittest/quantum_state/test_vector_type.py

echo "--- --- State normalisation --- ---"
python3 -m unittest quantum_state/unittest/quantum_state/test_normalization.py

echo "--- --- State equality --- ---"
python3 -m unittest quantum_state/unittest/quantum_state/test_equal.py

echo "--- --- Representation --- ---"
python3 -m unittest quantum_state/unittest/quantum_state/test_repr.py
