#!/bin/sh

# Validator module
echo "===================="
echo "| Validator Module |"
echo "===================="

echo "--- --- State vector validators --- ---"
python3 -m unittest quantum_state/unittest/validator/test_validator.py