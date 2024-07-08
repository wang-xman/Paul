#!/bin/sh

echo "========================"
echo "| Linear Object subpack |"
echo "========================"

echo "--- --- Linear object and validator --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_linear_object.py

echo "--- --- Linear object subtypes --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_types.py

echo "--- --- Algebra function decorator --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_decorator.py

echo "--- --- Linear Object Algebra Functions (LOAF) --- ---"
echo "--- --- --- LOAF : Transpose --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_trans.py

echo "--- --- --- LOAF : Norm --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_norm.py

echo "--- --- --- LOAF : Scale --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_scale.py

echo "--- --- --- LOAF : Inner --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_inner.py

echo "--- --- --- LOAF : Outer --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_outer.py

echo "--- --- --- LOAF : Dot --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_dot.py

echo "--- --- --- LOAF : Add --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_add.py

echo "--- --- --- LOAF : Sub --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_sub.py

echo "--- --- --- LOAF : Kronecker --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_kron.py

echo "--- --- --- LOAF : Multiply --- ---"
python3 -m unittest linear_space/unittest/linear_object/test_algebra_multiply.py