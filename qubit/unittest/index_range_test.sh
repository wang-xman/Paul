#!/bin/sh

echo "======================"
echo "| Index Range Module |"
echo "======================"

echo "--- --- Validators --- ---"
python3 -m unittest qubit/unittest/index_range/test_validators.py