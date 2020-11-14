# hamlibserver
## Description
Hamlib NET rigctl TCP server compatible with radio control applications. Implements rigctl commands. Adapted from hamlibserver.py by James Ahlstrom. Si5351 driver adapted from Hans Summers Si5351 demo code, translated from C to Python. Requires Adafruit CircuitPython and Si5351 libraries.

## Raspberry Pi Installation
Connect Raspberry Pi GPIO connector SCL, SDA, and GND pins to Si5351 board  
Raspberry Pi Configuration > Interfaces > I2C: Enable  
sudo apt install libhamlib2 libhamlib-utils python3-pip  
pip3 install RPI.GPIO  
pip3 install adafruit-blinka  
pip3 install adafruit-circuitpython-si5351  
Download and extract code from https://github.com/n7ihq/hamlibserver/archive/master.zip  

## Testing
python3 hamlibserver.py &  
rigctl —model=2 —rig-file=localhost:4575  
Commands:  

## Digital Modes Software Setup
### FLDIGI
Configure > Rig control > Rig > Hamlib >  
Rig: Hamlib NET rigctl  
Device: localhost:4575

### WSJT-X
File > Settings > Radio >  
Rig: Hamlib NET rigctl

## References
James Ahlstrom, "Hamlib, IPC and Software Defined Radio"  
http://www.james.ahlstrom.name/hamlib.html  

Hans Summers, "Si5351A Synthesizer demo code"  
https://www.qrp-labs.com/synth/si5351ademo.html

Adafruit CircuitPython Raspberry Pi library  
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi  
  
Adafruit CircuitPython Si5351 library  
https://learn.adafruit.com/adafruit-si5351-clock-generator-breakout/circuitpython  
