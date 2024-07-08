#!/bin/sh

# Braket module
echo "================="
echo "| Braket Module |"
echo "================="

echo "--- --- Bra, ket and related objects --- ---"
python3 -m unittest quantum_state/unittest/braket/test_braket.py