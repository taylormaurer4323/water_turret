from picamera2 import Picamera2, Preview
import time
from pynput.keyboard import Key, Listener
import RPi.GPIO as GPIO
import smbus

class water_turret:
    #Class constant vars
    cam_width_ = 640
    cam_height_ = 480
    rpi_gpio_solenoid_channel_ = 4
    rpi_smbus_id_ = 1
    servo_add_ = 0x2D
    up_down_servo_num_ = 1
    left_right_servo_num_ = 2
    angle_delta_ = 5
    up_limit_ = 160
    down_limit_ = 0
    right_limit_ = 25
    left_limit_ = 180
    
    def __init__(self, bDebug = False):
        #Param transfer
        self.bDebug_ = bDebug
        #Solenoid:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rpi_gpio_solenoid_channel_, GPIO.OUT)
        #servos
        self.servo_comm_bus_ = smbus.SMBus(self.rpi_smbus_id_)
        #picam
        self.picam2_  = Picamera2()
        camera_config = self.picam2_.create_still_configuration(main={"size": (self.cam_width_, self.cam_height_)}, display="main")
        self.picam2_.configure(camera_config)
        #Initialize the servo to default setting
        self.up_down_angle_ = 90
        self.IICServo_up_down()
        time.sleep(1)
        self.left_right_angle_ = 90
        self.IICServo_left_right()
        time.sleep(1)

    def IICServo_up_down(self):
        #Limit checking
        if self.up_down_angle_ < self.down_limit_:
            self.up_down_angle_ = self.down_limit_
            print('Minimum tilt angle reached: ', self.up_down_angle_)
        elif self.up_down_angle_ > self.up_limit_:
            self.up_down_angle_ = self.up_limit_
            print('Maximum tilt angle reached: ', self.up_down_angle_)
        
        if self.bDebug_:
            print('Setting angle to: ', self.up_down_angle_)
        self.servo_comm_bus_.write_byte_data(self.servo_add_, self.up_down_servo_num_, self.up_down_angle_)
        time.sleep(0.1)
        
    def IICServo_left_right(self):
        #Limit checking
        
        if self.left_right_angle_ > self.left_limit_:
            self.left_right_angle_ = self.left_limit_
            print('Minimum tilt angle reached: ', self.left_right_angle_)
        elif self.left_right_angle_ < self.right_limit_:
            self.left_right_angle_ = self.right_limit_
            print('Maximum tilt angle reached: ', self.left_right_angle_)
        
        if self.bDebug_:
            print('Setting angle to: ', self.left_right_angle_)
        self.servo_comm_bus_.write_byte_data(self.servo_add_, self.left_right_servo_num_, self.left_right_angle_)
        
    def interpret_keyboard(self, key):
        if key == Key.delete:
            return False
        elif key == Key.space:
            self.fire_water()
        elif key == Key.left:
            self.left_right_angle_ = self.left_right_angle_ + self.angle_delta_
            self.IICServo_left_right()
        elif key == Key.right:
            self.left_right_angle_ = self.left_right_angle_ - self.angle_delta_
            self.IICServo_left_right()
        elif key == Key.up:
            self.up_down_angle_ = self.up_down_angle_ + self.angle_delta_           
            self.IICServo_up_down()
        elif key == Key.down:
            self.up_down_angle_ = self.up_down_angle_ - self.angle_delta_
            self.IICServo_up_down()
            
    def fire_water(self):
        GPIO.output(self.rpi_gpio_solenoid_channel_, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(self.rpi_gpio_solenoid_channel_, GPIO.LOW)
        
    def run(self):
        self.picam2_.start_preview(Preview.QT)
        self.picam2_.start()    
        print('READY TO START RUNNING')
        with Listener(on_press = self.interpret_keyboard) as listener:
            listener.join()
        
def main():
    wt = water_turret(True)
    wt.run()
    
if __name__ == "__main__":
    main()