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

import time

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

# Write I2C block
def write_i2c_block(address, block):
    for i in range(retries):
        try:
            return bus.write_i2c_block_data(address, 1, block)
        except IOError:
            print ("IOError")
    return -1

# Read I2C byte
def read_i2c_byte(address):
    for i in range(retries):
        try:
            return bus.read_byte(address)
        except IOError:
            print ("IOError")
    return -1


# Read I2C block
def read_i2c_block(address):
    for i in range(retries):
        try:
            return bus.read_i2c_block_data(address, 1)
        except IOError:
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
	digital_reading = read_i2c_byte(address)
	return digital_reading

# Arduino Digital Write
def digitalWrite(pin, value):
	write_i2c_block(address, digitalWrite_cmd + [pin, value])
	return 1

# Read analog value from Pin
def analogRead(pin):
    write_i2c_block(address, analogRead_cmd + [pin, unused])
    analog_reading =  read_i2c_byte(address)
    return analog_reading
    # there's an issue getting block data
    # print read_i2c_block(address)
    #return number
    #return pinVal[1] * 255 + pinVal[2]

# Write PWM
def analogWrite(pin, value):
	write_i2c_block(address, analogWrite_cmd + [pin, value])
	return 1


if __name__ == '__main__': # only run if main program
    print ("testing pimaster")
    cont = 1
    while cont == 1:
        command = int(raw_input("what command index do you want? (6 for exit)"))
        print (command)

        if command in [1, 2, 3, 4, 5]:
            pin = int(raw_input("which pin?"))

        if command in [3, 5]:
            val = int(raw_input("what value to write?"))

        if command == 1:
            print ("set pin mode")
            mode = raw_input("what mode?")
            pinMode(pin, mode)
        elif command == 2:
            print ("digital read")
            print (digitalRead(pin))
        elif command == 3:
            print ("digital write")
            digitalWrite(pin, val)
        elif command == 4:
            print ("analog read")
            try:
                while True:
                    print (analogRead(pin))
                    time.sleep(.05)
            except KeyboardInterrupt:
                pass
        elif command == 5:
            print ("analog write")
            analogWrite(pin, val)
        elif command == 6:
            print ("bye bye tester")
            cont = 0
