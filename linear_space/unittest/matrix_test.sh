#!/bin/sh

# Matrix module
echo "=================="
echo "| Matrix Subpack |"
echo "=================="

echo "--- --- Matrix module --- ---"
python3 -m unittest linear_space/unittest/matrix/test_matrix.py

echo "--- --- Square matrix module --- ---"
python3 -m unittest linear_space/unittest/matrix/test_square.py

echo "--- --- Identity matrix module --- ---"
python3 -m unittest linear_space/unittest/matrix/test_identity.py