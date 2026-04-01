# Digiducky
This project is aimed to provide a simple solution to tranform a Digispark microcontroller to a rubberducky. My contribution to the digispark project is to provide a base script and a repo directory with the collection of tools designed to achieve this task.

## Base script functionnalities
- Convert duckyscript to arduino sketch source targeting digispark
- Convert binary scripts generated with duckencoder to arduino sketch for digispark

### Project Files
- /bin
- /exes
- /ino
- /scripts
- digiducky.py

### Requirements
- [Arduino IDE](https://www.arduino.cc/en/Main/Software) : to compile and upload the arduino generated sketch to the Digispark
- [Configuring the arduino IDE](https://digistump.com/wiki/digispark/tutorials/connecting) : to be able to detect the digispark in the arduino IDE
- [Python 2 or 3 installed](https://www.python.org/download/releases/3.0/) : Its better to use python 3

### Usage
1. Generate a duckyscript in the script directory or put any ducky script in the script folder
> echo "String Hello world" > scripts/examples.duck
2. Run the digiducky.py script
> Linux $ ./digiducky.py
3. Choose what conversion you want to make
> "1) Concert binary file to arduino script OR 2) Convert ducky script to arduino script"
4. Choose the file to convert

5. Open the folder with the script name and open the ino file with the arduino IDE

6. Click on upload and plug-in the digispark microcontroler

### Troubleshooting
By default on linux systems, when you run the arduino ide without root permision, upload the script and plug-in a digispark microcontroller, you get the following error :
>“micronucleus: library/micronucleus_lib.c:63: micronucleus_connect: Assertion `res >= 4' failed.”

This error is linked to the device permision once it is mounted. The device is mouted as root and as the arduino process is running with the current user previleges, yor are not able to upload the script to the controler.

The Digistump site has a page about [troubleshooting](https://digistump.com/wiki/digispark/tutorials/linuxtroubleshooting) this issue. You can also find some instructions here on how to [troubleshoot](https://digistump.com/board/index.php?topic=106.0) this issue.

#### Troubleshooting instructions :
The following instructions are inspired from the one given in [this](https://digistump.com/board/index.php?topic=106.0) tutorial.

1. Get your current user groups name (basicly choose the group with the same name as the username) with the command :
> groups "**your-username**"

2. Create the file **/etc/udev/rules.d/digispark.rules** and add the following lines to it
> SUBSYSTEM=="usb", ATTR{idVendor}=="16d0", ATTR{idProduct}=="0753", MODE="0660", GROUP="**your-username-or-group-here**"

3. Restart the device manager :
>sudo udevadm control --reload

Once this steps are done, click on upload and plugin the digispark. The script should now upload with no error.

### Sources
- hak5darren
  - [ducky scripts](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads)
  - [duckencoder.jar](https://github.com/hak5darren/USB-Rubber-Ducky/blob/master/duckencoder.jar)
- mame82
  - [duck2spark.py](https://github.com/mame82/duck2spark/blob/master/duck2spark.py)
  - [duckencoder.py](https://github.com/mame82/duckencoder.py/blob/master/duckencoder.py)
- Digistump
  - [Arduino digispark board configuration](https://digistump.com/wiki/digispark/tutorials/connecting)
- Amazon
  - [Digispark](https://www.amazon.fr/s/ref=nb_sb_noss_2/262-1600624-4223467?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=digispark)
