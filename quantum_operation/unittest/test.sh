#!/bin/sh

echo "*****************"
echo "* Package       *"
echo "*     Operation *"
echo "*****************"

# Gate operation
echo "=========================="
echo "| Gate Operation Subpack |"
echo "=========================="

echo "--- --- Memory validator --- ---"
python3 -m unittest quantum_operation/unittest/gate_operation/test_memory.py

echo "--- --- Operation object --- ---"
python3 -m unittest quantum_operation/unittest/gate_operation/test_operation.py

echo "--- --- Operation Launch method --- ---"
python3 -m unittest quantum_operation/unittest/gate_operation/test_launch.py


# Partial trace operation
echo "==================================="
echo "| Partial Trace Operation Subpack |"
echo "==================================="
echo "--- Partial tracing out a register ---"
python3 -m unittest quantum_operation/unittest/partial_trace/test_partial_tracing.py


# Measurement operation
echo "================================="
echo "| Measurement Operation Subpack |"
echo "================================="
echo "--- Operation validator ---"
python3 -m unittest quantum_operation/unittest/measurement/test_validator.py
echo "--- Measurment operation ---"
python3 -m unittest quantum_operation/unittest/measurement/test_operation.py


echo "**********************"
echo "**********************"