from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.start_recording('./my_video.rgba', format='rgba')

sleep(5)

camera.stop_recording()
camera.stop_preview()
