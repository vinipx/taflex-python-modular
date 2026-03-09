#!/bin/bash
# codechecks.sh - Script to check architecture and code coverage

echo "========================================="
echo "   Running Architecture & Coverage Checks"
echo "========================================="

echo ""
echo "[1/2] Checking Architecture (Maintainability Index) with Radon..."
radon mi . -s -i venv

echo ""
echo "[2/2] Running Code Coverage with Pytest..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest --cov=src/taflex tests/

echo ""
echo "========================================="
echo "   Code Checks Completed Successfully"
echo "========================================="
