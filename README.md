# Digiducky
This project provides a simple solution to transform a Digispark microcontroller into a rubber ducky. It includes a base script and a collection of tools to achieve this task.

## Features
- Convert DuckyScript to Arduino sketch targeting Digispark
- Convert binary scripts generated with DuckEncoder to Arduino sketch for Digispark

## Project Structure
```
├── bin/          # Compiled .bin payloads
├── exes/         # Conversion tools (duck2spark.py, digiducky_compile.sh, duckencoder.jar)
├── ino/          # Generated Arduino sketches
├── scripts/      # DuckyScript source files
└── digiducky.py  # Main entry point
```

## Requirements
- [Arduino IDE](https://www.arduino.cc/en/Main/Software) — to compile and upload the generated sketch to the Digispark
- [Configure Arduino IDE for Digispark](https://digistump.com/wiki/digispark/tutorials/connecting) — to detect the Digispark board
- [Python 3](https://www.python.org/downloads/) — Python 3 is required
- Java — required to run `duckencoder.jar`

## Usage
1. Place a DuckyScript in the `scripts/` directory:
```bash
echo "STRING Hello world" > scripts/example.duck
```
2. Run the main script:
```bash
./digiducky.py
```
3. Choose the conversion type:
   - `1` — Convert binary file to Arduino sketch
   - `2` — Convert DuckyScript to Arduino sketch
4. Follow the prompts to select the file and keyboard mapping.
5. Open the generated `.ino` file from the `ino/` folder in the Arduino IDE.
6. Click **Upload** and plug in the Digispark when prompted.

## Troubleshooting
On Linux, running the Arduino IDE without root privileges may produce:
```
micronucleus: library/micronucleus_lib.c:63: micronucleus_connect: Assertion `res >= 4' failed.
```
This is a USB device permission issue. Fix it by creating a udev rule:

1. Find your group name:
```bash
groups <your-username>
```
2. Create `/etc/udev/rules.d/digispark.rules` with:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="16d0", ATTR{idProduct}=="0753", MODE="0660", GROUP="<your-group>"
```
3. Reload udev rules:
```bash
sudo udevadm control --reload
```

Then click Upload and plug in the Digispark. See the [Digistump troubleshooting page](https://digistump.com/wiki/digispark/tutorials/linuxtroubleshooting) for more details.

## Security Notes
- All file paths are validated to prevent path traversal attacks.
- External commands are executed using argument lists (no shell interpolation).
- Only Python 3 is supported.

## Sources
- hak5darren — [DuckyScript payloads](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads), [duckencoder.jar](https://github.com/hak5darren/USB-Rubber-Ducky/blob/master/duckencoder.jar)
- mame82 — [duck2spark.py](https://github.com/mame82/duck2spark/blob/master/duck2spark.py), [duckencoder.py](https://github.com/mame82/duckencoder.py/blob/master/duckencoder.py)
- Digistump — [Arduino Digispark board configuration](https://digistump.com/wiki/digispark/tutorials/connecting)
