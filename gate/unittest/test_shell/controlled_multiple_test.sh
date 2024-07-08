#!/bin/sh

# Controlled operation
echo "========================="
echo "| Controlled Operations |"
echo "========================="

echo "--- --- Decorator global operator matrix method --- ---"
python3 -m unittest gate/unittest/controlled/test_global_operator_matrix.py

echo "=========================="
echo "| Controlled Single Gate |"
echo "=========================="

echo "--- --- Controlled single gate --- ---"
python3 -m unittest gate/unittest/controlled/test_singles.py

echo "========================="
echo "| Controlled Multi Gate |"
echo "========================="

echo "--- --- Controlled multiple-qubit gate --- ---"
python3 -m unittest gate/unittest/controlled/test_multiples.py