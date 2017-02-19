"""
vision.py
=========

Used to stream video and stuff.
"""

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from PIL import Image


class DriverVision(object):

    def make_jpeg_from_frame(self, frame):
        """Converts an OpenCV frame to a JPEG buffer."""
        if frame is None or not frame.any():
            return 'none'

        image = Image.fromarray(frame)
        buf = StringIO()
        image.save(buf, 'JPEG')
        return buf.getvalue()

    def get_frame_from_targeting(self, module, make_jpeg=True):
        """Fetches the current frame from the camera."""
        frame = module.last_frame

        if make_jpeg:
            return self.make_jpeg_from_frame(frame)
        else:
            return frame
