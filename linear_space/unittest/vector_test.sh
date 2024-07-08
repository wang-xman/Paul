#!/bin/sh

echo "=================="
echo "| Vector Subpack |"
echo "=================="

echo "--- --- Base vector validator and class --- ---"
python3 -m unittest linear_space/unittest/vector/test_basevector.py

echo "--- --- Column vector validator and class --- ---"
python3 -m unittest linear_space/unittest/vector/test_columnvector.py

echo "--- --- Row Vector related classes --- ---"
python3 -m unittest linear_space/unittest/vector/test_rowvector.py

echo "--- --- Unit vector class --- ---"
python3 -m unittest linear_space/unittest/vector/test_unitvector.py

echo "--- --- Standard basis vector class --- ---"
python3 -m unittest linear_space/unittest/vector/test_standardbasis.py