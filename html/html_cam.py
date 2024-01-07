from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2

from libcamera import controls
from libcamera import Transform
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration({"size": (640, 480)}, transform=Transform(vflip=True))
picam2.configure(camera_config)
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
encoder = H264Encoder(bitrate=1000000, repeat=True, iperiod=15)
#output = FfmpegOutput("-f hls -hls_time 0 -hls_list_size 2 -hls_flags delete_segments -hls_allow_cache 0 stream.m3u8")
output = FfmpegOutput("-f rtsp -rtsp_transport tcp rtsp://localhost:8001/live.stream")
#output = FfmpegOutput("-f mpegts tcp://192.168.31.158:1234")
picam2.start_recording(encoder, output)
time.sleep(9999999)

