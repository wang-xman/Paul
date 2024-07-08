#!/bin/sh

echo "=================="
echo "| Number subpack |"
echo "=================="

echo "--- --- Types --- ---"
python3 -m unittest linear_space/unittest/number/test_type_checking.py

echo "--- --- Power of two --- ---"
python3 -m unittest linear_space/unittest/number/test_power.py
