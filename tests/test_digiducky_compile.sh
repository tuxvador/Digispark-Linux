#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "$0")
ROOT_DIR=$(realpath "$SCRIPT_DIR/..")

TEST_DUCK=$(mktemp /tmp/test_XXXXXX.duck)
TEST_INO=$(mktemp /tmp/test_XXXXXX.ino)
cleanup() {
    rm -f "$TEST_DUCK" "$TEST_INO"
}
trap cleanup EXIT

echo "=== Testing digiducky_compile.sh ==="

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

python3 "$ROOT_DIR/exes/digiducky_compile.py" "$TEST_DUCK" "$TEST_INO"

echo "Verifying generated sketch..."

grep -q '#include "DigiKeyboard.h"' "$TEST_INO" && echo "  PASS: includes DigiKeyboard.h" || { echo "  FAIL: missing include"; exit 1; }
grep -q 'void setup()' "$TEST_INO" && echo "  PASS: has setup()" || { echo "  FAIL: missing setup()"; exit 1; }
grep -q 'void loop()' "$TEST_INO" && echo "  PASS: has loop()" || { echo "  FAIL: missing loop()"; exit 1; }
grep -q 'DigiKeyboard.print("Hello World");' "$TEST_INO" && echo "  PASS: has STRING output" || { echo "  FAIL: missing STRING"; exit 1; }
grep -q 'DigiKeyboard.delay(1000);' "$TEST_INO" && echo "  PASS: has DELAY (100ms * 10)" || { echo "  FAIL: missing DELAY"; exit 1; }
grep -q 'KEY_MODIFIER_LEFT_GUI' "$TEST_INO" && echo "  PASS: has GUI modifier" || { echo "  FAIL: missing GUI"; exit 1; }

SETUP_COUNT=$(grep -c 'void setup()' "$TEST_INO")
if [ "$SETUP_COUNT" -eq 1 ]; then
    echo "  PASS: single setup()"
else
    echo "  FAIL: expected 1 setup(), found $SETUP_COUNT"
    exit 1
fi

echo ""
echo "All digiducky_compile.sh tests passed!"
