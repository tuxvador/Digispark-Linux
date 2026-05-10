#!/usr/bin/env python3
# Coding : utf-8
"""
    Script : ducky2spark
    Version : 1.1
    function : convert ducky scripts to binary and arduino files
"""

import os
import subprocess
import glob

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

VALID_MAPPINGS = ["be","ca","ch","de","dk","es","fr","gb","it","no","pt","ru","sv","uk","us"]

cf2c = "\nChoose file to convert : "
cb2i = "Convert ducky script to arduino script"
cd2i = "Convert binary file to arduino script"
cu2i = "Upload sketch to Digispark"
wiyc = "\nWhat is your choice : "
choosemapping = "Choose keyboard mapping to use : "

def _safe_path(base, filename):
    base = os.path.realpath(os.path.abspath(base if os.path.isabs(base) else os.path.join(BASE_DIR, base)))
    full = os.path.realpath(os.path.abspath(os.path.join(base, os.path.basename(filename))))
    if not full.startswith(base + os.sep):
        raise ValueError("Invalid path: " + filename)
    return full

def _get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Enter a number.")

def choosefile(path):
    files = [f for f in glob.glob(path + "**/*", recursive=True) if os.path.isfile(f)]

    for i, j in enumerate(files):
        print(str(i+1) + ") " + os.path.relpath(j, path))
    choix = -1
    while choix not in range(len(files)):
        choix = _get_int(cf2c) - 1
    return files[choix]

def duckToIno():
    mapping = ""
    filepath = choosefile(os.path.join(BASE_DIR, "scripts") + "/")
    filename = os.path.splitext(os.path.basename(filepath))[0]
    while mapping not in VALID_MAPPINGS:
        mapping = input(choosemapping)
    bin_path = _safe_path("bin", filename + ".bin")
    cmd = ["java", "-jar", os.path.join(BASE_DIR, "exes", "duckencoder.jar"),
           "-i", filepath, "-o", bin_path, "-l", mapping]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    binToIno(bin_path)

def binToIno(path):
    directory = os.path.splitext(os.path.basename(path))[0]
    ino_dir = _safe_path("ino", directory)
    print("Dir : " + directory)
    if not os.path.isdir(ino_dir):
        os.mkdir(ino_dir)
    ino_file = _safe_path(ino_dir, directory + ".ino")
    cmd = ["python3", os.path.join(BASE_DIR, "exes", "duck2spark.py"),
           "-i", path, "-l", "1", "-o", ino_file]
    subprocess.run(cmd, check=True)

def upload_ino():
    filepath = choosefile(os.path.join(BASE_DIR, "ino") + "/")
    cmd = ["bash", os.path.join(BASE_DIR, "exes", "upload.sh"), filepath]
    subprocess.run(cmd)

def main():
    choix = 0
    while choix not in [1, 2, 3]:
        print("1) " + cd2i)
        print("2) " + cb2i)
        print("3) " + cu2i)
        choix = _get_int(wiyc)
    if choix == 1:
        binToIno(choosefile(os.path.join(BASE_DIR, "bin") + "/"))
    elif choix == 2:
        duckToIno()
    elif choix == 3:
        upload_ino()

if __name__ == '__main__':
    main()
