#!/bin/sh

echo "================"
echo "| Qubit Module |"
echo "================"

echo "--- --- Generic qubit state --- ---"
python3 -m unittest qubit/unittest/qubit/test_qubit.py

echo "--- --- Qubit state superposition --- ---"
python3 -m unittest qubit/unittest/qubit/test_qubit_superposition.py

echo "--- --- Computational basis --- ---"
python3 -m unittest qubit/unittest/qubit/test_computational_basis.py