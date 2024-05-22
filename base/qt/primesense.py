import numpy as np
from primesense import openni2
from primesense.openni2 import *
from primesense._openni2 import *
from .qtcv import *

class PrimeSensePlayer(VideoPlayerBase):
    def __init__(self, dev=0, depth_size=(640,480), rgb_size=(320,240), fps=30, *args, **kws):
        super().__init__(*args, **kws)
        self.fps = fps
        self.depth_w, self.depth_h = depth_size
        self.rgb_w, self.rgb_h = rgb_size
        openni2.initialize()
        d = openni2.Device.open_any()

        self.depth_stream = d.create_depth_stream()
        self.depth_stream.set_property(ONI_STREAM_PROPERTY_VIDEO_MODE, OniVideoMode(pixelFormat=OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=depth_size[0], resolutionY=depth_size[1], fps=fps))
        assert self.depth_stream is not None

        self.rgb_stream = d.create_color_stream()
        self.rgb_stream.set_property(ONI_STREAM_PROPERTY_VIDEO_MODE, OniVideoMode(pixelFormat=OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=rgb_size[0], resolutionY=rgb_size[1], fps=fps))

        self.start()

    def __del__(self):
        self.stop()
        openni2.unload()

    def start(self):
        if self.is_running:
            self.stop()
        self.depth_stream.start()
        self.rgb_stream.start()
        super().start()

    def stop(self):
        super().stop()
        if self.is_running:
            self.depth_stream.stop()
            self.rgb_stream.stop()

    def get_frame(self):
        s = openni2.wait_for_any_stream([self.rgb_stream, self.depth_stream], 2)
        depth_frame = self.depth_stream.read_frame()
        rgb_frame = self.rgb_stream.read_frame()

        d = depth_frame.get_buffer_as_uint16()
        depth_map = np.reshape(d, (self.depth_h, -1))

        d = rgb_frame.get_buffer_as_uint8()
        rgb_img = np.reshape(d, (self.rgb_h, -1, 3))
        rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
        if rgb_img.shape[:2] != depth_map.shape[:2]:
            imh, imw = depth_map.shape[:2]
            rgb_img = cv2.resize(rgb_img, (imw, imh))

        return  rgb_img, depth_map
