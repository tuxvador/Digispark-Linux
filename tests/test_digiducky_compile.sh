#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "$0")
ROOT_DIR=$(realpath "$SCRIPT_DIR/..")

echo "=== Testing digiducky_compile.sh ==="

# Generate a simple test DuckyScript
TEST_DUCK=$(mktemp /tmp/test_XXXXXX.duck)
TEST_INO=$(mktemp /tmp/test_XXXXXX.ino)

cat > "$TEST_DUCK" << 'EOF'
REM Test payload
STRING Hello World
ENTER
DELAY 100
GUI r
DELAY 500
STRING notepad
ENTER
EOF

# Run the compiler
bash "$ROOT_DIR/exes/digiducky_compile.sh" "$TEST_DUCK" "$TEST_INO"

# Verify output
echo "Verifying generated sketch..."

grep -q '#include "DigiKeyboard.h"' "$TEST_INO" && echo "  PASS: includes DigiKeyboard.h"
grep -q 'void setup()' "$TEST_INO" && echo "  PASS: has setup()"
grep -q 'void loop()' "$TEST_INO" && echo "  PASS: has loop()"
grep -q 'DigiKeyboard.print("Hello World");' "$TEST_INO" && echo "  PASS: has STRING output"
grep -q 'DigiKeyboard.delay(1000);' "$TEST_INO" && echo "  PASS: has DELAY (100ms * 10)"
grep -q 'KEY_MODIFIER_LEFT_GUI' "$TEST_INO" && echo "  PASS: has GUI modifier"

# Verify no duplicate setup
SETUP_COUNT=$(grep -c 'void setup()' "$TEST_INO")
if [ "$SETUP_COUNT" -eq 1 ]; then
    echo "  PASS: single setup()"
else
    echo "  FAIL: expected 1 setup(), found $SETUP_COUNT"
    exit 1
fi

rm -f "$TEST_DUCK" "$TEST_INO"
echo ""
echo "All digiducky_compile.sh tests passed!"
