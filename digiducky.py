#!/usr/bin/env python3
# Coding : utf-8
"""
    Script : ducky2spark
    Version : 1.1
    function : convert ducky scripts to binary and arduino files
"""

import os
import subprocess

VALID_MAPPINGS = ["be","ca","ch","de","dk","es","fr","gb","it","no","pt","ru","sv","uk","us"]

cf2c = "\nChoose file to convert : "
cb2i = "Convert ducky script to arduino script"
cd2i = "Convert binary file to arduino script"
wiyc = "\nWhat is your choice : "
choosemapping = "Choose keyboard mapping to use : "

def _safe_path(base, filename):
    """Resolve path and ensure it stays within base directory."""
    base = os.path.realpath(os.path.abspath(base))
    full = os.path.realpath(os.path.abspath(os.path.join(base, os.path.basename(filename))))
    if not full.startswith(base + os.sep):
        raise ValueError("Invalid path: " + filename)
    return full

def choosefile(path):
    files = []
    for entry in os.walk(path):
        files = entry[2]
        break

    for i, j in enumerate(files):
        print(str(i+1) + ") " + j)
    choix = -1
    while choix not in range(len(files)):
        choix = int(input(cf2c)) - 1
    return _safe_path(path, files[choix])

def duckToIno():
    mapping = ""
    filepath = choosefile("./scripts/")
    filename = os.path.splitext(os.path.basename(filepath))[0]
    while mapping not in VALID_MAPPINGS:
        mapping = input(choosemapping)
    bin_path = _safe_path("./bin", filename + ".bin")
    cmd = ["java", "-jar", "./exes/duckencoder.jar", "-i", filepath,
           "-o", bin_path, "-l", mapping]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    binToIno(bin_path)

def binToIno(path):
    path = os.path.realpath(path)
    directory = os.path.splitext(os.path.basename(path))[0]
    ino_dir = _safe_path("./ino", directory)
    print("Dir : " + directory)
    if not os.path.isdir(ino_dir):
        os.mkdir(ino_dir)
    ino_file = _safe_path(ino_dir, directory + ".ino")
    cmd = ["python3", "./exes/duck2spark.py", "-i", path, "-l", "1", "-o", ino_file]
    subprocess.run(cmd, check=True)

def main():
    choix = 0
    while choix not in [1, 2]:
        print("1) " + cd2i)
        print("2) " + cb2i)
        choix = int(input(wiyc))
    if choix == 1:
        binToIno(choosefile("./bin/"))
    if choix == 2:
        duckToIno()

if __name__ == '__main__':
    main()
