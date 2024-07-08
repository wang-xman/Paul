#!/bin/sh

# Qubit validators
echo "===================="
echo "| Validator Module |"
echo "===================="

echo "--- --- Qubit state validator --- ---"
python3 -m unittest qubit/unittest/validators/test_qubit_state_validator.py

echo "--- --- Single qubit state validator --- ---"
python3 -m unittest qubit/unittest/validators/test_single_qubit_basis_validator.py