#!/bin/sh

# Helper functions module
echo "============================"
echo "| Algebra function subpack |"
echo "============================"

echo "--- --- LSAF : Scale --- ---"
python3 -m unittest linear_space/unittest/algebra/test_scale.py

echo "--- --- LSAF : Norm --- ---"
python3 -m unittest linear_space/unittest/algebra/test_norm.py

echo "--- --- LSAF : Inner product --- ---"
python3 -m unittest linear_space/unittest/algebra/test_inner.py

echo "--- --- LSAF : Outer product --- ---"
python3 -m unittest linear_space/unittest/algebra/test_outer.py

echo "--- --- LSAF : Kronecker product --- ---"
python3 -m unittest linear_space/unittest/algebra/test_kronecker.py

echo "--- --- LSAF : Transpose --- ---"
python3 -m unittest linear_space/unittest/algebra/test_transpose.py

echo "--- --- LSAF : Complex conjugate --- ---"
python3 -m unittest linear_space/unittest/algebra/test_complex_conjugate.py

echo "--- --- LSAF : Hermitian conjugate --- ---"
python3 -m unittest linear_space/unittest/algebra/test_hermitian_conjugate.py

echo "--- --- LSAF : Matrix product --- ---"
python3 -m unittest linear_space/unittest/algebra/test_matrix_product.py