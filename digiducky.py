#!/usr/bin/python
# Coding : utf-8
"""
    Script : ducky2spark
    Version : 1.0
    function : convert ducky scripts to binary and arduino files
"""

#imports
import os
from fnmatch import fnmatch
from subprocess import Popen,PIPE

#Strings used in programme
cf2c = "\nChoose file to convert : "
cb2i = "Convert ducky script to arduino script"
cd2i = "Concert binary file to arduino script"
wiyc = "\nWhat is your choice : "
convbin = "Converting file to bin"
convino = "Converting file to ino"
duckencoder = "java -jar ./exes/duckencoder.jar -i "
ducky2spark = "python ./exes/duck2spark.py -i "
choosemapping = "Choose keyboard mapping to use : "

def choosefile(path):
    files = []
    length = 0

    for files in os.walk(path):
        length = len(files)
        files = files[2]

    choix = -1
    for i,j in enumerate(files):
        print(str(i+1)+") "+j)
    while choix not in range(0,length):
        choix = int(raw_input(cf2c))-1
    path = path+files[choix]+" "
    return path

def duckToIno():
    global duckencoder
    mapping = ""
    path = choosefile("./scripts/")
    filename = path[10:-6]
    while mapping not in ["be","ca","ch","de","dk","es","fr","gb","it","no","pt","ru","sv","uk","us"]:
        mapping = raw_input(choosemapping)
    duckencoder = duckencoder+path+"-o ./bin/"+filename+".bin -l "+mapping
    filename = "./bin/"+filename+".bin"
    execute = os.popen(duckencoder).read()
    print(execute)
    binToIno(filename)

def binToIno(path):
    global ducky2spark
    directory = path[6:-4]
    isdir = os.path.isdir("./ino/"+directory)
    print("Dir : "+directory)
    if(isdir == False):
        os.mkdir("./ino/"+directory)
    ducky2spark = ducky2spark+path+" -l 1 -o ./ino/"+directory+"/"+directory+".ino"
    #print(ducky2spark)
    execute = os.system(ducky2spark)

def main():
    choix = ""
    while(choix not in [1,2]):
        print("1) "+cd2i)
        print("2) "+cb2i)
        choix = int(raw_input(wiyc))
    if choix == 1:
        binToIno(choosefile("./bin/"))
    if choix == 2:
        duckToIno()

if __name__ == '__main__':
    main()
