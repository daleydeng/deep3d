import numpy as np
from realsense import pyrealsense2 as rs
from ..realsense import rs_probe_fov, rs_create_pipeline
from .qtcv import *

class RealSensePlayer(VideoPlayerBase):
    def __init__(self, dev=0, depth_size=(640,480), depth_fps=90, color_size=(960,540), color_fps=60, align_to='', *args, **kws):
        super().__init__(*args, **kws)
        self.fps = max(depth_fps, color_fps)
        self.depth_w, self.depth_h = depth_size
        self.color_w, self.color_h = color_size

        self.pipeline, self.config, (self.depth_fov, self.color_fov) = rs_create_pipeline(depth_size, depth_fps, color_size, color_fps)

        if align_to == 'color':
            self.align = rs.align(rs.stream.color)
            self.depth_fov = self.color_fov
        elif align_to == 'depth':
            self.align = rs.align(rs.stream.depth)
            self.color_fov = self.depth_fov
        else:
            self.align = None

        self.is_running = False

    def __del__(self):
        self.stop()

    def start(self):
        if self.is_running:
            return

        profile = self.pipeline.start(self.config)
        self.is_running = True

    def stop(self):
        if self.is_running:
            self.pipeline.stop()
            self.is_running = False

    def get_frame(self):
        if not self.is_running:
            return -1

        frames = self.pipeline.wait_for_frames()
        if self.align:
            frames = self.align.process(frames)
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            return None

        depth_map = np.asanyarray(depth_frame.get_data())
        color_img = np.asanyarray(color_frame.get_data())

        return color_img, depth_map
