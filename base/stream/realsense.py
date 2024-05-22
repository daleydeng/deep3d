import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
import numpy as np
import realsense.pyrealsense2 as rs
from ..realsense import rs_create_pipeline

class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, depth_size=(640,480), depth_fps=90, color_size=(960,540), color_fps=60, use_align=True, **kws):
        super().__init__(**kws)
        self.pipeline, self.config, (depth_fov, color_fov) = rs_create_pipeline(depth_size, depth_fps, color_size, color_fps)
        print ("pipeline created")
        if use_align:
            self.align = rs.align(rs.stream.color)
        else:
            self.align = False

        self.color_dur = 1 / color_fps * Gst.SECOND
#         self.launch_string = f'''
# appsrc name=source is-live=true block=true format=GST_FORMAT_TIME caps=video/x-raw,format=RGB,width={color_size[0]},height={color_size[1]},framerate={color_fps}/1
#         ! videoconvert ! video/x-raw,format=I420
#         ! x264enc speed-preset=ultrafast tune=zerolatency
#         ! rtph264pay config-interval=1 name=pay0 pt=96
# '''
        self.launch_string = f'''
        videotestsrc
        ! video/x-raw,format=I420,rate=30,width=320,height=240
        ! x264enc tune=zerolatency
        ! rtph264pay name=pay0 pt=96
'''

        self.start()

    def __del__(self):
        if hasattr(self, 'pipeline'):
            self.stop()

    def start(self):
        self.pipeline.start(self.config)
    def stop(self):
        self.pipeline.stop()

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.frame_nr = 0
        # appsrc = rtsp_media.get_element().get_child_by_name('source')
        # appsrc.connect('need-data', self.on_need_data)

    def on_state_changed(self, bus, msg):
        old, new, pending = msg.parse_state_changed()
        print ("here", old, new, pending)
        if new == Gst.State.PLAYING:
            self.start()
        elif new == Gst.State.PAUSED:
            self.stop()

    def on_need_data(self, src, length):
        frames = self.pipeline.wait_for_frames()
        if self.align:
            frames = self.align.process(frames)
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return

        depth_map = np.asanyarray(depth_frame.get_data())
        color_img = np.asanyarray(color_frame.get_data())

        data = color_img.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.color_dur
        timestamp = self.frame_nr * self.color_dur
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp

        self.frame_nr += 1
        retval = src.emit('push-buffer', buf)
        print (f"pushed buffer, {self.frame_nr}, duration {self.color_dur/Gst.SECOND}")
        if retval != Gst.FlowReturn.OK:
            print (retval)

class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, point='/live', properties={}, **kws):
        super().__init__(**properties)
        self.factory = SensorFactory(**kws)
        self.factory.set_shared(True)
        self.get_mount_points().add_factory(point, self.factory)
        self.attach(None)

def run_server(cls=GstServer, **kws):
    GObject.threads_init()
    Gst.init(None)
    server = cls(**kws)
    loop = GObject.MainLoop()
    loop.run()
