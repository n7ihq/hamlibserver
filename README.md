# hamlibserver
## Description
Hamlib NET rigctl TCP server compatible with radio control applications. Implements Hamlib rigctl commands. Adapted from hamlibserver.py by James Ahlstrom. Si5351 driver adapted from Hans Summers Si5351 demo code, translated from C to Python. Requires Adafruit CircuitPython and Si5351 libraries.

## Raspberry Pi Installation
Disconnect existing Si5351 controller  
Connect Raspberry Pi GPIO connector SCL, SDA, and GND pins to Si5351 board  
Raspberry Pi Configuration > Interfaces > I2C: Enable  
sudo apt install libhamlib2 libhamlib-utils python3-pip  
pip3 install RPI.GPIO  
pip3 install adafruit-blinka  
pip3 install adafruit-circuitpython-si5351  
Download and extract code from https://github.com/n7ihq/hamlibserver/archive/master.zip  

## Testing
python3 hamlibserver.py &  
rigctl -m 2 -r 127.0.0.1:4575  
### Commands
F, set_freq ’Frequency': Set ’Frequency’, in Hz  
f, get_freq: Get ’Frequency’, in Hz  
m, get_mode: Get ’Mode’ ’Passband'    
v, get_vfo: Get current ’VFO’  
q, exit: Exit rigctl in interactive mode

## Digital Modes Software Settings
### FLDIGI
Configure > Rig control > Rig > Hamlib >  
Use Hamlib: check  
Rig: Hamlib NET rigctl  
Device: 127.0.0.1:4575  
Retry Interval (mSec): 100

### WSJT-X, JS8Call
File > Settings > Radio >  
Rig: Hamlib NET rigctl  
Cat Control Network Server: 127.0.0.1:4575

## To Do
Add Si5351 calibration dialog

## References
James Ahlstrom, "Hamlib, IPC and Software Defined Radio"  
http://www.james.ahlstrom.name/hamlib.html  

Hans Summers, "Si5351A Synthesizer demo code"  
https://www.qrp-labs.com/synth/si5351ademo.html

Adafruit CircuitPython Raspberry Pi library  
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi  
  
Adafruit CircuitPython Si5351 library  
https://learn.adafruit.com/adafruit-si5351-clock-generator-breakout/circuitpython  
