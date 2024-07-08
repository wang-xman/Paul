#!/bin/sh
echo "*****************"
echo "* Package       *"
echo "*    Bit Object *"
echo "*****************"

# Validator module
echo "===================="
echo "| Validator Module |"
echo "===================="

echo "--- --- Validators --- ---"
python3 -m unittest bit/unittest/test_validators.py

# Utility function module
echo "=================="
echo "| Utility Module |"
echo "=================="
echo "--- --- Utility functions --- ---"
python3 -m unittest bit/unittest/test_utils.py

# Bistring module
echo "=========================="
echo "| Bistring Object Module |"
echo "=========================="
echo "--- --- Bitstring object --- ---"
python3 -m unittest bit/unittest/test_bitstring_object.py

# Bislist module
echo "========================="
echo "| Bislist Object Module |"
echo "========================="
echo "--- --- Bitstring object --- ---"
python3 -m unittest bit/unittest/test_bitlist_object.py

# Bitrange module
echo "=========================="
echo "| Bisrange Object Module |"
echo "=========================="
echo "--- --- Bitrange bound validator --- ---"
python3 -m unittest bit/unittest/test_bitrange.py

echo "**********************"
echo "**********************"