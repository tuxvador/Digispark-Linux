#!/bin/bash
set -e

usage() {
    cat <<'EOF'
Usage: ./exes/upload.sh <sketch.ino>

Compiles and uploads an Arduino sketch to a Digispark board.

Requirements:
  - arduino-cli (compile + upload): https://arduino.github.io/arduino-cli/
  - micronucleus (upload only): sudo apt install micronucleus

Examples:
  ./exes/upload.sh ino/notepad/notepad.ino
  ./exes/upload.sh scripts/example.duck           # auto-convert then upload
EOF
    exit 1
}

if [ $# -lt 1 ]; then usage; fi
INPUT=$(realpath "$1")
if [ ! -f "$INPUT" ]; then echo "Error: file not found: $INPUT"; exit 1; fi

# Auto-convert .duck files before uploading
if [[ "$INPUT" == *.duck ]]; then
    echo "Converting DuckyScript to Arduino sketch..."
    python3 digiducky.py --upload "$INPUT"
    exit $?
fi

SKETCH_DIR=$(dirname "$INPUT")
SKETCH_NAME=$(basename "$INPUT" .ino)

# --- Compile ---
if command -v arduino-cli &>/dev/null; then
    echo "Compiling $INPUT..."
    if ! arduino-cli core list 2>/dev/null | grep -q digistump; then
        echo "Installing Digistump AVR core..."
        arduino-cli core install digistump:avr
    fi
    BUILD_DIR=$(mktemp -d)
    arduino-cli compile --fqbn digistump:avr:digispark-tiny --build-path "$BUILD_DIR" "$SKETCH_DIR"
    HEX=$(find "$BUILD_DIR" -name "*.hex" | head -1)
    if [ -z "$HEX" ]; then
        echo "Error: compiled .hex not found in $BUILD_DIR"
        rm -rf "$BUILD_DIR"
        exit 1
    fi
elif [ -f "${SKETCH_DIR}/${SKETCH_NAME}.hex" ]; then
    HEX="${SKETCH_DIR}/${SKETCH_NAME}.hex"
    echo "Using existing .hex: $HEX"
else
    echo "Error: arduino-cli not found and no .hex file available."
    echo "Install arduino-cli: https://arduino.github.io/arduino-cli/"
    exit 1
fi

# --- Upload ---
if command -v micronucleus &>/dev/null; then
    echo "Uploading $HEX to Digispark..."
    echo "Plug in the Digispark when prompted..."
    micronucleus --run "$HEX"
    echo "Upload complete!"
else
    echo "micronucleus not found. Install it:"
    echo "  sudo apt install micronucleus"
    echo ""
    echo "Then manually upload:"
    echo "  micronucleus --run $HEX"
    exit 1
fi

# Cleanup temp build dir
if [ -n "$BUILD_DIR" ]; then rm -rf "$BUILD_DIR"; fi
