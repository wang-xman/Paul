#!/bin/sh
echo "************************"
echo "* Package              *"
echo "*     Quantum Operator *"
echo "************************"

# Generic module
echo "=================="
echo "| Generic Module |"
echo "=================="

echo "--- --- Initialisation --- ---"
python3 -m unittest quantum_operator/unittest/test_generic.py

echo "--- --- Default apply method --- ---"
python3 -m unittest quantum_operator/unittest/test_apply.py