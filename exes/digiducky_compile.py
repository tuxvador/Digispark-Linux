#!/usr/bin/env python3
import sys
import os
import re

PREAMBLE = '''\
#include "DigiKeyboard.h"

// Delay between keystrokes
#define KEYSTROKE_DELAY 1000


#define  KEY_ESC         0x29  // Escape
#define KEY_MODIFIER_LEFT_GUI 0x08

int iterationCounter = 0;


void setup() {
\t// initialize the digital pin as an output.
\tpinMode(0, OUTPUT); //LED on Model B
\tpinMode(1, OUTPUT); //LED on Model A     
\tdigitalWrite(0, LOW);
\tdigitalWrite(1, LOW);
\tDigiKeyboard.update();
\t// this is generally not necessary but with some older systems it seems to
\t// prevent missing the first character after a delay:
\tDigiKeyboard.sendKeyStroke(0);

\t// It's better to use DigiKeyboard.delay() over the regular Arduino delay()
\t// if doing keyboard stuff because it keeps talking to the computer to make
\t// sure the computer knows the keyboard is alive and connected
\tDigiKeyboard.delay(KEYSTROKE_DELAY);

'''

POSTAMBLE = '''\
void loop(){
\tdelay(1000);
\titerationCounter++;
}
'''

MODIFIER_MAP = {
    "GUI": "KEY_MODIFIER_LEFT_GUI",
    "WINDOWS": "KEY_MODIFIER_LEFT_GUI",
    "SHIFT": "KEY_MODIFIER_LEFT_SHIFT",
    "ALT": "KEY_MODIFIER_LEFT_ALT",
    "CONTROL": "KEY_MODIFIER_LEFT_CTRL",
    "CTRL": "KEY_MODIFIER_LEFT_CTRL",
}

KEY_MAP = {
    "MENU": "PROPS",
    "APP": "PROPS",
    "LEFTARROW": "LEFT",
    "RIGHTARROW": "RIGHT",
    "UPARROW": "UP",
    "DOWNARROW": "DOWN",
    "ESCAPE": "ESC",
}


def compile_duckyscript(infile, outfile):
    with open(outfile, "w") as out:
        out.write(PREAMBLE)

        with open(infile) as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue

                parts = line.split()
                command = parts[0]

                if command == "REM":
                    comment = line[4:] if len(line) > 4 else ""
                    out.write(f"  //{comment}\n")

                elif command == "STRING":
                    text = line[7:] if len(line) > 7 else ""
                    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
                    out.write(f'\tDigiKeyboard.print("{escaped}");\n')

                elif command == "DELAY":
                    try:
                        ms = int(parts[1]) * 10
                    except (IndexError, ValueError):
                        ms = 0
                    out.write(f"  DigiKeyboard.delay({ms});\n")

                else:
                    out.write(_parse_key_stroke(parts))

        out.write("\t}\n\n")
        out.write(POSTAMBLE)


def _parse_key_stroke(tokens):
    modifiers = ["0"]
    key1 = None
    key2 = None

    for token in tokens:
        upper = token.upper()
        if upper in MODIFIER_MAP:
            modifiers.append(MODIFIER_MAP[upper])
        else:
            mapped = KEY_MAP.get(upper, token)
            if key1 is None:
                key1 = f"KEY_{mapped.upper()}"
            else:
                key2 = f"KEY_{mapped.upper()}"

    mod_str = " | ".join(modifiers)
    k1 = key1 or "0"
    k2 = key2 or "0"
    return f"  DigiKeyboard.sendKeyStroke({k1}, {k2}, {mod_str});\n"


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.duck> <output.ino>")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    if not os.path.isfile(infile):
        print(f"Error: input file not found: {infile}")
        sys.exit(1)

    compile_duckyscript(infile, outfile)


if __name__ == "__main__":
    main()
