#!/bin/sh
# Single-qubit gates
echo "======================"
echo "| Single Gate Module |"
echo "======================"

echo "--- --- Pauli X --- ---"
python3 -m unittest gate/unittest/singles/test_X.py

echo "--- --- Pauli Y --- ---"
python3 -m unittest gate/unittest/singles/test_Y.py

echo "--- --- Pauli Z --- ---"
python3 -m unittest gate/unittest/singles/test_Z.py

echo "--- --- Flip --- ---"
python3 -m unittest gate/unittest/singles/test_flip.py

echo "--- --- Walsh - Hadamard --- ---"
python3 -m unittest gate/unittest/singles/test_hadamard.py

echo "--- --- Phase --- ---"
python3 -m unittest gate/unittest/singles/test_phase.py

echo "--- --- One-eighth pi --- ---"
python3 -m unittest gate/unittest/singles/test_eighthpi.py

echo "--- --- Rotation about x (Rx) --- ---"
python3 -m unittest gate/unittest/singles/test_Rx.py

echo "--- --- Rotation about y (Ry) --- ---"
python3 -m unittest gate/unittest/singles/test_Ry.py

echo "--- --- Rotation about z (Rz) --- ---"
python3 -m unittest gate/unittest/singles/test_Rz.py

echo "--- --- Phase rotation with parameters --- ---"
python3 -m unittest gate/unittest/singles/test_phase_rotation.py