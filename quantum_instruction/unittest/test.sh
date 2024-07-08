#!/bin/sh

echo "***************************"
echo "* Package                 *"
echo "*     Quantum Instruction *"
echo "***************************"

# Base module
echo "==================================="
echo "| Quantum Instruction Base Module |"
echo "==================================="

# Gate-operation instruction module
echo "====================================="
echo "| Gate-Operation Instruction Module |"
echo "====================================="
echo "--- Module Loaction : /quantum_instruction/gate_instruction.py ---"
echo "--- --- Gate subdict validator --- ---"
python3 -m unittest quantum_instruction/unittest/gate/test_gate_subdict.py
echo "--- --- Target subdict validator --- ---"
python3 -m unittest quantum_instruction/unittest/gate/test_target_subdict.py
echo "--- --- Control subdict validator --- ---"
python3 -m unittest quantum_instruction/unittest/gate/test_control_subdict.py
echo "--- --- Gate-operation instruction validator --- ---"
python3 -m unittest quantum_instruction/unittest/gate/test_instruction_validator.py
echo "--- --- Gate-operation instruction OBJECT --- ---"
python3 -m unittest quantum_instruction/unittest/gate/test_instruction.py


# Partial-trace-operation instruction module
echo "=============================================="
echo "| Partial-Trace-Operation Instruction Module |"
echo "=============================================="
echo "--- Module Location : /quantum_instruction/partial_trace_instruction.py ---"
echo "--- --- Instruction dict validator --- ---"
python3 -m unittest quantum_instruction/unittest/partial_trace/test_validators.py
echo "--- --- Instruction object --- ---"
python3 -m unittest quantum_instruction/unittest/partial_trace/test_instruction.py


# Measurement instruction module
echo "============================================"
echo "| Measurement-Operation Instruction Module |"
echo "============================================"
echo "--- Module Location : /quantum_instruction/measurement_instruction.py ---"
echo "--- --- Measurement instruction validator --- ---"
python3 -m unittest quantum_instruction/unittest/measurement/test_validator.py
echo "--- --- Measurement instruction object --- ---"
python3 -m unittest quantum_instruction/unittest/measurement/test_instruction.py

echo "**********************"
echo "**********************"