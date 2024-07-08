#!/bin/sh

# Null state module
echo "====================="
echo "| Null State Module |"
echo "====================="

echo "--- --- Singleton null state --- ---"
python3 -m unittest quantum_state/unittest/null_state/test_null_state.py