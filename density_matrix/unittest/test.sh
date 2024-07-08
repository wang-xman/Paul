#!/bin/sh

echo "**********************"
echo "* Pacakge            *"
echo "*     Density Matrix *"
echo "**********************"

echo "========================="
echo "| Density Matrix Module |"
echo "========================="

echo "--- --- Validator --- ---"
python3 -m unittest density_matrix/unittest/test_validator.py

echo "--- --- Initialisation --- ---"
python3 -m unittest density_matrix/unittest/test_init.py

#echo "--- --- Algebra --- ---"
#python3 -m unittest density_matrix/unittest/test_algebra.py