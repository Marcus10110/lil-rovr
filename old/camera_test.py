import time
import picamera2
camera = picamera2.Picamera2()
camera.start()

time.sleep(2)
metadata = camera.capture_file("test.jpg")
print(metadata)

camera.close()
