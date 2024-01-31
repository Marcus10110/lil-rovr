import io
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, MJPEGEncoder, H264Encoder
from picamera2.outputs import FileOutput


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class CameraStream():
    def __init__(self) -> None:
        self._picam2 = Picamera2()
        self._picam2.configure(
            self._picam2.create_video_configuration(main={"size": (640, 480)}))
        self._output = StreamingOutput()
        # self._picam2.start_recording(JpegEncoder(), FileOutput(self._output))
        self._picam2.start_recording(H264Encoder(), FileOutput(self._output))

    def get_frame(self):
        with self._output.condition:
            self._output.condition.wait()
            frame = self._output.frame
            return frame
