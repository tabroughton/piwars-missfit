#!/usr/bin/env python
#
# i2c master for interfacing with atmega328-firmware slave
#
# http://www.digitalpolymath.co.uk/
# Tom Broughton
#

#set up the i2c system management bus
import smbus
bus = smbus.SMBus(1)

# I2C Address of ATMEGA328-slave
address = 0x04

# Commands to send to slave
pinMode_cmd = [1]
digitalRead_cmd = [2]
digitalWrite_cmd = [3]
analogRead_cmd = [4]
analogWrite_cmd = [5]

# Slave is set to read 3 bytes so we'll send unused to fill buffer
unused = 0
# retries before we decide we have IO Error through connection issue
retries = 10

debug = False
# set debug mode (default off)
def set_debugMode(on_off):
    if on_off == 1 or on_off == 0:
        debug = on_off;
    if debug == True:
        print ("debug mode on")

# Write I2C block
def write_i2c_block(address, block):
	for i in range(retries):
		try:
			return bus.write_i2c_block_data(address, 1, block)
		except IOError:
			if debug:
				print ("IOError")
	return -1

# Read I2C byte
def read_i2c_byte(address):
	for i in range(retries):
		try:
			return bus.read_byte(address)
		except IOError:
			if debug:
				print ("IOError")
	return -1


# Read I2C block
def read_i2c_block(address):
	for i in range(retries):
		try:
			return bus.read_i2c_block_data(address, 1)
		except IOError:
			if debug:
				print ("IOError")
	return -1


# Setting Up Pin mode on Arduino
def pinMode(pin, mode):
	if mode == "OUTPUT":
		write_i2c_block(address, pinMode_cmd + [pin, 1])
	elif mode == "INPUT":
		write_i2c_block(address, pinMode_cmd + [pin, 0])
	return 1

# Arduino Digital Read
def digitalRead(pin):
	write_i2c_block(address, digitalRead_cmd + [pin, unused])
	pinVal = read_i2c_byte(address)
	return pinVal

# Arduino Digital Write
def digitalWrite(pin, value):
	write_i2c_block(address, digitalWrite_cmd + [pin, value])
	return 1


# Read analog value from Pin
def analogRead(pin):
	write_i2c_block(address, ananlogRead_cmd + [pin, unused])
	read_i2c_byte(address)
    # analog values may be greater than 255 and we are dealing with bytes
	pinVal = read_i2c_block(address)
	return pinVal[1] * 255 + pinVal[2]


# Write PWM
def analogWrite(pin, value):
	write_i2c_block(address, analogWrite_cmd + [pin, value])
	return 1
