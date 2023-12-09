import RPi.GPIO as GPIO
import time

#set using the GPIO numbers (I think)
GPIO.setmode(GPIO.BCM)
CHANNEL = 4
GPIO.setup(CHANNEL, GPIO.OUT)


if __name__ == '__main__':
	
	GPIO.output(CHANNEL, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(CHANNEL, GPIO.LOW)	
