# hamlibserver
## Description
Hamlib NET rigctl TCP server compatible with radio control applications. Implements Hamlib ? commands. Adapted from hamlibserver.py by James Ahlstrom. Si5351 driver adapted from Hans Summers Si5351 demo code, translated from C to Python. Uses Adafruit CircuitPython and Si5351 libraries.
## Raspberry Pi Installation
Connect Raspberry Pi GPIO connector SCL, SDA, and GND pins to Si5351 board
Download and extract code from https://github.com/n7ihq/hamlibserver/archive/master.zip
sudo apt install libhamlib2 libhamlib-utils python3-pip
Enable Raspberry Pi I2C interface
pip3 install RPI.GPIO
pip3 install adafruit-blinka
pip3 install adafruit-circuitpython-si5351
## Testing
python3 hamlibserver.py &
rigctl —model=2 —rig-file=localhost:4575
Commands: 
## FLDIGI Setup
## WSJT-X Setup
## JS8Call Setup
## Reference
