#!/bin/sh

echo "***************************"
echo "* Package                 *"
echo "*     Quantum Measurement *"
echo "***************************"

# Validator
echo "===================="
echo "| Validator Module |"
echo "===================="

#echo "--- --- Bit range validator --- ---"
#python3 -m unittest measurement/unittest/test_validator.py

# Partial trace
echo "========================"
echo "| Partial Trace Module |"
echo "========================"

echo "--- --- Manually perform partial trace --- ---"
python3 -m unittest measurement/unittest/partial_trace/test_manual.py

echo "--- --- Partial trace function --- ---"
python3 -m unittest measurement/unittest/partial_trace/test_function.py

# Projective measurement
echo "================================="
echo "| Projective Measurement Module |"
echo "================================="

echo "--- --- Single projective measurement --- ---"
python3 -m unittest measurement/unittest/projective/test_single_measurement.py

echo "--- --- All projective measurement --- ---"
python3 -m unittest measurement/unittest/projective/test_all.py

echo "**********************"
echo "**********************"