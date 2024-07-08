#!/bin/sh

echo "*********************"
echo "* Package           *"
echo "*     Superposition *"
echo "*********************"

echo "===================="
echo "| Superlist Module |"
echo "===================="
echo "--- --- Superlist validators --- ---"
python3 -m unittest superposition/unittest/test_superlist.py


echo "========================"
echo "| Superposition Module |"
echo "========================"
echo "--- --- Superposition validators --- ---"
python3 -m unittest superposition/unittest/test_superposition_validator.py

echo "--- --- Superposition objects --- ---"
python3 -m unittest superposition/unittest/test_superposition.py

echo "*********************"
echo "*********************"