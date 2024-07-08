#!/bin/sh

echo "**********************"
echo "* Package            *"
echo "*     Quantum Flow   *"
echo "**********************"

# Base module
echo "==============="
echo "| Base Module |"
echo "==============="

echo "--- --- Base Quantum Flow --- ---"
python3 -m unittest quantum_flow/unittest/base/test_base_flow.py

# Quantum flow module
echo "======================="
echo "| Quantum Flow Module |"
echo "======================="
echo "--- --- Launch quantum flow on memory --- ---"
python3 -m unittest quantum_flow/unittest/quantum_flow/test_launch_on_memory.py
echo "--- --- Apply unified matrix to global state --- ---"
python3 -m unittest quantum_flow/unittest/quantum_flow/test_unified_matrix.py


# Dedicated flow makers
echo "========================="
echo "| Dedicated Flow Makers |"
echo "========================="
echo ""

echo "====================================="
echo "| Walsh-Hadamard Gate Related Flows |"
echo "====================================="
echo "--- --- Hadamard flow on register --- ---"
python3 -m unittest quantum_flow/unittest/walsh_hadamard/test_hadamard_register.py
echo "--- --- Hadamard flow on memory --- ---"
python3 -m unittest quantum_flow/unittest/walsh_hadamard/test_hadamard_memory.py

echo "==========================="
echo "| SWAP Gate Related Flows |"
echo "==========================="
echo "--- --- SWAP flow --- ---"
python3 -m unittest quantum_flow/unittest/swap/test_swap.py
echo "--- --- Overall SWAP flow --- ---"
python3 -m unittest quantum_flow/unittest/swap/test_overall_swap.py


echo "==========================================="
echo "| Quantum Fourier Transform Related Flows |"
echo "==========================================="
echo "--- --- Quantum Fourier flow --- ---"
python3 -m unittest quantum_flow/unittest/fourier/test_qft_register.py

echo "================================="
echo "| Reflection About a State Flow |"
echo "================================="
echo "--- --- Reflection flow --- ---"
python3 -m unittest quantum_flow/unittest/reflection/test_reflection_zeros.py

echo "**********************"
echo "**********************"