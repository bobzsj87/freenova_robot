from picamera2 import Picamera2, Preview
from libcamera import Transform

import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(transform=Transform(vflip=True))
picam2.configure(camera_config)
#picam2.start_preview(Preview.DRM)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")
