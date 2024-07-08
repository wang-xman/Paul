#!/bin/sh

echo "************************"
echo "* Package              *"
echo "*     Quantum register *"
echo "************************"

# Base
echo "==============="
echo "| Base Module |"
echo "==============="

echo "--- --- Base register --- ---"
python3 -m unittest quantum_register/unittest/test_base.py

echo "===================="
echo "| Registers Module |"
echo "===================="

echo "--- --- Different types of registers --- ---"
python3 -m unittest quantum_register/unittest/test_registers.py

echo "**********************"
echo "**********************"