#!/bin/sh

echo "**********************"
echo "* Package            *"
echo "*     Quantum Memory *"
echo "**********************"


# Base module
echo "==============="
echo "| Base Module |"
echo "==============="
echo "--- --- Validators --- ---"
python3 -m unittest quantum_memory/unittest/test_validator.py

# Metadata module
echo "==================="
echo "| Metadata Module |"
echo "==================="
echo "--- --- Base register metadata --- ---"
python3 -m unittest quantum_memory/unittest/test_base_register_metadata.py

# Memory module
echo "================="
echo "| Memory Module |"
echo "================="
echo "--- --- Base memory class --- ---"
python3 -m unittest quantum_memory/unittest/test_base_memory.py

# Manager module
echo "================="
echo "| Manager Module |"
echo "================="
echo "--- --- Register manager --- ---"
python3 -m unittest quantum_memory/unittest/test_register_manager.py
echo "--- --- Index manager --- ---"
python3 -m unittest quantum_memory/unittest/test_index_manager.py

echo "======================="
echo "| Qubit Memory Module |"
echo "======================="
echo "--- --- Qubit register metadata --- ---"
python3 -m unittest quantum_memory/unittest/test_qubit_register_metadata.py
echo "--- --- Qubit memory object --- ---"
python3 -m unittest quantum_memory/unittest/test_qubit_memory.py

echo "**********************"
echo "**********************"
