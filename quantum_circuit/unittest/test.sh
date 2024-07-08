#!/bin/sh

echo "***********************"
echo "* Pacakge             *"
echo "*     Quantum Circuit *"
echo "***********************"

# Grover search
echo "========================="
echo "| Grover Search Circuit |"
echo "========================="
echo "--- --- Integrated circuit --- ---"
python3 -m unittest quantum_circuit/unittest/grover/test_grover.py

# Phase estimation 
echo "============================"
echo "| Phase Estimation Circuit |"
echo "============================"
echo "--- --- Phase estimation via flows --- ---"
python3 -m unittest quantum_circuit/unittest/phase_estimation/test_pe.py

echo "***********************"
echo "***********************"