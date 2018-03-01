"""
    Control TB6612FNG motor drivers via Atmega328 connected to RPi via i2C
    Date: 28/02/2018
    Atuhor: Tom Broughton
    Intention of this script is to test the motor control
    the main function to call is motorCMD(mCMD) with below text commands

"""

import pi2c
from time import sleep

class Motor:
    """ Deals with single motor output on a sparkfun monster moto shield.
        * sparkfun monster moto shield - no need for ENPin
        * TB6612FNG breakout - needs ENPin
    """

    HIGH = 1
    LOW = 0

    def __init__(self, CWPin, CCWPin, PWMPin, ENPin=-1, Speed=0, Direction="CW"):
        """ Creates an instance of a motor.
            :param CWPin:
                The pin driving clockwise motoion
            :param CCWPin:
                The pin on the motor driver driving counterclockwise motoion
            :param PWMPin:
                The pin varying the speed of the motor
            :param ENPin:
                The pin that enables the motor (default is -1 if not needed)
            :Speed:
                The initial speed to set the motor 0-255 - note a negative value
                will result in a counterclockwise direction.
            :Direction:
                The default direction of the motor, alternative can be CCW
        """
        self.cwPin = CWPin
        self.ccwPin = CCWPin
        self.pwmPin = PWMPin
        self.enPin = ENPin
        self.maxSpeed = 255
        self.minSpeed = -255
        self.lastSpeed = 0
        self.speed = 0

        pi2c.pinMode(self.cwPin, "OUTPUT")
        pi2c.pinMode(self.ccwPin, "OUTPUT")
        pi2c.pinMode(self.pwmPin, "OUTPUT")
        if self.enPin > -1:
            pi2c.pinMode(self.enPin, "OUTPUT")

        self.set_speed(Speed)
        self.set_direction(Direction)

    def set_speed(self, Speed):
        """ Sets the speed of the motor.
            :param Speed:
                A value (between 255 and -255) mapped to the voltage of the motor.
                A negative value will result in counterclockwise direction of motor.
        """
        if Speed == self.lastSpeed: return
        self.lastSpeed = Speed
        if Speed > self.maxSpeed:
            self.speed = self.maxSpeed
        elif Speed < self.minSpeed:
            self.speed = self.minSpeed
        else:
            self.speed = Speed

        if self.speed < 0:
            self.set_direction("CCW")
            self.speed = -self.speed
        else:
            self.set_direction("CW")

    def set_direction(self, Direction):
        """ Sets the direction of the motor, either clockwise or
            counterclockwise.
            params: Direction can be "CW" or "CCW"
        """
        if Direction != "CW" and Direction != "CCW": return
        self.direction = Direction

    def on(self):
        """ Turns the motor on.
        """
        if self.direction == "CW":
            pi2c.digitalWrite(self.cwPin, Motor.HIGH)
            pi2c.digitalWrite(self.ccwPin, Motor.LOW)
        else:
            pi2c.digitalWrite(self.ccwPin, Motor.HIGH)
            pi2c.digitalWrite(self.cwPin, Motor.LOW)
        pi2c.analogWrite(self.pwmPin, int(self.speed))
        if self.enPin > -1:
            pi2c.digitalWrite(self.enPin, Motor.HIGH)

    def off(self):
        """ Turns the motor off.
        """
        print("turning motor off")
        if self.enPin > -1:
            pi2c.digitalWrite(self.enPin, Motor.LOW)
        pi2c.digitalWrite(self.cwPin, Motor.LOW)
        pi2c.digitalWrite(self.ccwPin, Motor.LOW)
        pi2c.analogWrite(self.pwmPin, Motor.LOW)

    def get_speed(self): return self.speed
    def get_direction(self): return self.direction

class Driver(object):
    """ Super class for all motor driver classes, drives the motors attached
        to the monster moto shield.
    """

    def __init__(self):
        """ Creates an instance of the motor driver and two instances of motor.
        """
        self.driving = False
        self.motorLeft = Motor(8, 7, 9, 6)
        self.motorRight = Motor(4, 3, 5, 2)

    def drive(self, SpeedLeft, SpeedRight):
        """ Called to drive both left and right motors.
            :param SpeedLeft:
                The speed at which the left motor should turn.
            :param SpeedRight:
                The speed at which the right motor should turn.
        """
        print("Speeds %d, %d" % (SpeedLeft, SpeedRight))
        self.motorLeft.set_speed(SpeedLeft)
        self.motorRight.set_speed(SpeedRight)
        self.motorLeft.on()
        self.motorRight.on()

    def stop(self):
        """ Turns off both motors to stop the robot.
        """
        print("driver off")
        self.motorLeft.off()
        self.motorRight.off()
        self.driving = False

    def start(self):
        """ Called to start the driver, simply sets the driving to true so that
            this attribute can be returned later to determin if driver is in
            action.
        """
        print("driver on")
        self.driving = True

    def __del__(self):
        """ Deconstructor ensure we stop the motors if script ends or class no
            longer needed."""
        self.stop()

class Keyboard_Driver(object):
    """ an interface to drive via user keyboard
    """
    def __init__(self):
        self.driver = Driver()

    def invalidCMD(self):
        print("Invalid command")

    def action(self, CMD):
        """ captures action from keyboard
            :param CMD:
                the key command from keyboard
                F = forward
                B = backward
                R = right
                L = left
                S = stop
        """
        if CMD == 'F':
            self.driver.drive(125, 125)
        elif CMD == 'B':
            self.driver.drive(-125, -125)
        elif CMD == 'R':
            self.driver.drive(-100, 100)
        elif CMD == 'L':
            self.driver.drive(100, -100)
        elif CMD == 'S':
            self.driver.stop()
        else:
            self.invalidCMD()


if __name__ == '__main__':
    try:
        kDriver = Keyboard_Driver()
    except Exception as e:
        print(str(e))

    while 1:
        try:
            #store any data from the command line input
            kData = input("Enter Motor Command: ")
            if kData: kDriver.action(kData)

        except KeyboardInterrupt:
            kDriver.action('S');
            break

        except Exception as e:
            print(str(e))
        	# Turn motors off
            kDriver.action('S');
            break
