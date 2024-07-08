#!/bin/sh

# Superposition
echo "=================================="
echo "| (Quantum) Superposition Module |"
echo "=================================="

echo "--- --- Superposition validator --- ---"
python3 -m unittest quantum_state/unittest/superposition/test_superposition_validator.py

echo "--- --- Superposition object and related classes --- ---"
python3 -m unittest quantum_state/unittest/superposition/test_superposition.py