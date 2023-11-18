from gpiozero import LED
from time import sleep





def main1():
    led = LED(27)

    while True:
        led.off()
        sleep(1)
        led.on()
        sleep(1)
        
    

if __name__ == '__main__':
    main1()