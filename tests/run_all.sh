#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "$0")
echo "========================================"
echo "  Digispark-Linux Test Suite"
echo "========================================"
echo ""

# Python tests
echo ">>> Running duck2spark tests..."
python3 "$SCRIPT_DIR/test_duck2spark.py"
echo ""

# Shell tests
echo ">>> Running digiducky_compile tests..."
bash "$SCRIPT_DIR/test_digiducky_compile.sh"
echo ""

echo "========================================"
echo "  All tests passed!"
echo "========================================"
