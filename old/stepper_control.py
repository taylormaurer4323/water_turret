import time
import _thread
import threading
import atexit
import sys
import termios
import contextlib
import RPi.GPIO as GPIO
#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
#example w/the hat library
#mh = Adafruit_MotorHAT()
#myStepper = mh.getStepper(200,1)
#myStepper.setSpeed(40)


#myStepper.step(200, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)




#mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
#mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
#mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
#mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)



#example:
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
#initialize the motorkit class
kit = MotorKit()
#there are two stepper motors within the class
#stepper1: corresponds to M1 and M2 terminals
#stepper2: corresponds to M3 and M4

#the following is a single coil step
#kit.stepper1.onestep()
#the following releases control of coils reducing power draw
#kit.stepper1.release()
#kit.stepper2.release()
#kit.stepper1.release()
for i in range(200):
    kit.stepper2.onestep(direction=stepper.FORWARD)
    time.sleep(.01)

kit.stepper2.release()  