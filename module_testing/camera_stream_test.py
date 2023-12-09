from picamera2 import Picamera2, Preview
import time
#Create picam2
picam2 = Picamera2()
#create cam config
camera_config = picam2.create_still_configuration(main={"size": (2592, 1944)}, lores={"size":(640, 480)}, display="lores")
#load config
picam2.configure(camera_config)
picam2.start_preview(Preview.QT)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")


