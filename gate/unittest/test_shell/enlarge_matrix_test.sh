#!/bin/sh

echo "=================================="
echo "| Matrix Enlarge : Noncontrolled |"
echo "=================================="

echo "--- --- Single-qubit gate matrix --- ---"
python3 -m unittest gate/unittest/enlarge_matrix/test_single_qubit_matrix.py

echo "--- --- Multiple-qubit gate matrix --- ---"
python3 -m unittest gate/unittest/enlarge_matrix/test_multiple_qubit_matrix.py

# Enlarge matrix
echo "==============================="
echo "| Matrix Enlarge : Controlled |"
echo "==============================="

echo "--- --- Generic validator --- ---"
python3 -m unittest gate/unittest/enlarge_matrix/test_validator.py

echo "--- --- Kernel function --- ---"
python3 -m unittest gate/unittest/enlarge_matrix/test_kernel.py

echo "--- --- CISWAP routines --- ---"
python3 -m unittest gate/unittest/enlarge_matrix/test_ciswap.py

echo "--- --- Single-Controlled Multiple-Qubit (SCMQ) --- ---"
python3 -m unittest gate/unittest/enlarge_matrix/test_scmq.py