#!/bin/sh

echo "====================="
echo "| Prototype Subpack |"
echo "====================="

echo "--- --- Prototype validators --- ---"
python3 -m unittest gate/unittest/prototype_base/test_validator.py

echo "--- --- Inherited prototype class --- ---"
python3 -m unittest gate/unittest/prototype_base/test_inherited_prototype.py

echo "--- --- Base prototype --- ---"
python3 -m unittest gate/unittest/prototype_base/test_prototype.py