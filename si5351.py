# Author: Jim Larsen, 2020
# Adapted from Hans Summers Si5351a C code example
# Website: http:www.hanssummers.com

# A very very simple Si5351a demonstration
# Please also refer to SiLabs AN619 which describes all the registers to use

import board
import busio
import adafruit_si5351

XTAL_FREQ = 25000000
i2c = busio.I2C(board.SCL, board.SDA)
si5351 = adafruit_si5351.SI5351(i2c)

# Set up PLL A with mult, num and denom
# mult is 15..90
# num is 0..1,048,575
# denom is 0..1,048,575

# Set CLK0 output ON and to the specified frequency
# Frequency is in the range 1MHz to 150MHz
# Example: setFrequency(10000000);
# will set output CLK0 to 10MHz

# This example sets up PLL A
# and MultiSynth 0
# and produces the output on CLK0

def setFrequency(frequency):

	xtalFreq = XTAL_FREQ
	
	divider = int(900000000 / frequency) # Calculate the division ratio. 900,000,000 is the maximum internal 
									# PLL frequency: 900MHz
	if (divider % 2): divider -= 1	# Ensure an even integer division ratio
	pllFreq = divider * frequency	# Calculate the pllFrequency: the divider * desired output frequency
	mult = int(pllFreq / xtalFreq)	# Determine the multiplier to get to the required pllFrequency
	l = int(pllFreq % xtalFreq)		# It has three parts:
	f = l							# mult is an integer that must be in the range 15..90
	f *= 1048575					# num and denom are the fractional parts, the numerator and denominator
	f /= xtalFreq					# each is 20 bits (range 0..1048575)
	num = int(f)					# the actual multiplier is  mult + num / denom
	denom = 1048575					# For simplicity we set the denominator to the maximum 1048575

	# Set up PLL A with the calculated multiplication ratio
	# Reset the PLL. This causes a glitch in the output. For small changes to 
	# the parameters, you don't need to reset the PLL, and there is no glitch
	si5351.pll_a.configure_fractional(mult, num, denom)

	# Set up MultiSynth divider 0, with the calculated divider
	# Set the MultiSynth0 input to be PLL A
	# The final R division stage can divide by a power of two, from 1..128. 
	# reprented by constants R_DIV1 to R_DIV128
	# If you want to output frequencies below 1MHz, you have to use the 
	# final R division stage
	# Reset the PLL.
	si5351.clock_0.configure_integer(si5351.pll_a, divider)	
									
	# Finally switch on the CLK0 output
	si5351.outputs_enabled = True

def getFrequency():
	if si5351.clock_0.frequency == None:	# Si5351 not initialized
		setFrequency(28000000)
	return si5351.clock_0.frequency

if __name__ == "__main__":
	print("Clock0 frequency:", getFrequency())
	setFrequency(10000000)	# Set frequency to 10 MHz
	print("Clock0 frequency:", getFrequency())
