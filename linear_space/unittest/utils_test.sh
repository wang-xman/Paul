#!/bin/sh

echo "============================"
echo "| Utility function subpack |"
echo "============================"

echo "--- --- Linear Object : Verifiers--- ---"
python3 -m unittest linear_space/unittest/utils/test_verifiers.py

echo "--- --- Maker module --- ---"
python3 -m unittest linear_space/unittest/utils/test_makers.py
