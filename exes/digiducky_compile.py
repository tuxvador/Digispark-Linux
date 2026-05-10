#!/usr/bin/env python3
import sys
import os

PREAMBLE = """\
#include "DigiKeyboard.h"

// Delay between keystrokes
#define KEYSTROKE_DELAY 1000


#define  KEY_ESC         0x29  // Escape
#define KEY_MODIFIER_LEFT_GUI 0x08

int iterationCounter = 0;


void setup() {
    // initialize the digital pin as an output.
    pinMode(0, OUTPUT); //LED on Model B
    pinMode(1, OUTPUT); //LED on Model A
    digitalWrite(0, LOW);
    digitalWrite(1, LOW);
    DigiKeyboard.update();
    // this is generally not necessary but with some older systems it seems to
    // prevent missing the first character after a delay:
    DigiKeyboard.sendKeyStroke(0);

    // It's better to use DigiKeyboard.delay() over the regular Arduino delay()
    // if doing keyboard stuff because it keeps talking to the computer to make
    // sure the computer knows the keyboard is alive and connected
    DigiKeyboard.delay(KEYSTROKE_DELAY);

"""

POSTAMBLE = """\
void loop(){
    delay(1000);
    iterationCounter++;
}
"""

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

SINGLE_KEY_COMMANDS = {
    "ENTER": "KEY_ENTER",
    "SPACE": "KEY_SPACE",
    "TAB": "KEY_TAB",
    "CAPSLOCK": "KEY_CAPS_LOCK",
    "DELETE": "KEY_DELETE",
    "BACKSPACE": "KEY_BACKSPACE",
    "HOME": "KEY_HOME",
    "END": "KEY_END",
    "INSERT": "KEY_INSERT",
    "PAGEUP": "KEY_PAGEUP",
    "PAGEDOWN": "KEY_PAGEDOWN",
    "ESC": "KEY_ESC",
    "ESCAPE": "KEY_ESC",
    "PRINTSCREEN": "KEY_PRINT_SCREEN",
    "SCROLLLOCK": "KEY_SCROLL_LOCK",
    "PAUSE": "KEY_PAUSE",
    "NUMLOCK": "KEY_NUM_LOCK",
    "BREAK": "KEY_PAUSE",
}


def compile_duckyscript(infile, outfile):
    with open(infile) as f:
        lines = f.readlines()

    with open(outfile, "w") as out:
        out.write(PREAMBLE)
        last_line = None

        for line in lines:
            line = line.rstrip("\n")
            if not line.strip():
                continue

            parts = line.split()
            command = parts[0].upper()

            if command == "REM":
                comment = line[3:] if len(line) > 3 else ""
                out.write(f"    //{comment}\n")

            elif command == "STRING":
                text = line[6:] if len(line) > 6 else ""
                text = text.lstrip()
                escaped = text.replace("\\", "\\\\").replace('"', '\\"')
                emitted = f'    DigiKeyboard.print("{escaped}");\n'
                out.write(emitted)
                last_line = emitted

            elif command == "DELAY":
                try:
                    ms = int(parts[1]) * 10
                except (IndexError, ValueError):
                    ms = 0
                emitted = f"    DigiKeyboard.delay({ms});\n"
                out.write(emitted)
                last_line = emitted

            elif command == "REPEAT":
                if last_line is not None:
                    try:
                        count = int(parts[1]) - 1
                    except (IndexError, ValueError):
                        count = 0
                    for _ in range(count):
                        out.write(last_line)

            else:
                emitted = _parse_key_stroke(parts)
                out.write(emitted)
                if command not in ("REPEAT",):
                    last_line = emitted

        out.write("    }\n\n")
        out.write(POSTAMBLE)


def _parse_key_stroke(tokens):
    modifiers = ["0"]
    key1 = None
    key2 = None

    for token in tokens:
        upper = token.upper()
        if upper in MODIFIER_MAP:
            modifiers.append(MODIFIER_MAP[upper])
        elif upper in SINGLE_KEY_COMMANDS:
            mapped = SINGLE_KEY_COMMANDS[upper]
            if key1 is None:
                key1 = mapped
            else:
                key2 = mapped
        else:
            mapped = KEY_MAP.get(upper, token)
            if key1 is None:
                key1 = f"KEY_{mapped.upper()}"
            else:
                key2 = f"KEY_{mapped.upper()}"

    mod_str = " | ".join(modifiers)
    k1 = key1 or "0"
    k2 = key2 or "0"
    return f"    DigiKeyboard.sendKeyStroke({k1}, {k2}, {mod_str});\n"


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
