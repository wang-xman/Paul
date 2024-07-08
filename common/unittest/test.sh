#!/bin/sh
echo "***************************************"
echo "* Package                             *"
echo "*     Application-wide Common Objects *"
echo "***************************************"

# Exception module
echo "===================="
echo "| Exception Module |"
echo "===================="
echo "--- --- Customised exceptions --- ---"
python3 -m unittest common/unittest/test_exception.py



# Validator module
echo "===================="
echo "| Validator Module |"
echo "===================="
echo "--- --- Validators in common module --- ---"
python3 -m unittest common/unittest/test_validator.py


# Parameter module
echo "===================="
echo "| Parameter Module |"
echo "===================="
echo "--- --- Parameter related --- ---"
python3 -m unittest common/unittest/test_parameter.py


# String module
echo "================="
echo "| String Module |"
echo "================="
echo "--- --- String verifier --- ---"
python3 -m unittest common/unittest/test_string.py


# Function module
echo "===================="
echo "| Function Subpack |"
echo "===================="
echo "--- --- Function signature analyzer --- ---"
python3 -m unittest common/unittest/test_function.py

echo "--- --- Function decorators --- ---"
python3 -m unittest common/unittest/test_decorators.py

echo "***************************************"
echo "***************************************"