import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import time

class VideoPlayerBase(QThread):
    sig_frame = pyqtSignal(object, int)
    sig_finished = pyqtSignal()

    def __init__(self, fps=60, *args, **kws):
        super().__init__(*args, **kws)
        self.clear()
        self.fps = fps

    def clear(self):
        self.is_running = False
        self.cur_idx = -1
        self.cur_frame = None

    def get_frame(self):
        flag, frame = self.cap.read()
        if flag:
            return frame

    def run(self):
        self.is_running = True
        while self.is_running:
            start_t = time.time()
            self.cur_idx += 1
            tic = time.time()
            frame = self.get_frame()
            if frame is None:
                self.clear()
                return

            self.cur_frame = frame
            self.sig_frame.emit(frame, self.cur_idx)
            proc_t = time.time() - tic
            t_step = 1/self.fps
            if proc_t < t_step:
                time.sleep(t_step-proc_t)

    def stop(self):
        self.is_running = False
        self.wait()

class VideoPlayer(VideoPlayerBase):
    def __init__(self, cap, fps=-1, *args, **kws):
        super().__init__(*args, **kws)
        if not isinstance(cap, cv2.VideoCapture):
            cap = cv2.VideoCapture(cap)
        self.cap = cap
        if fps < 0:
            fps = max(cap.get(cv2.CAP_PROP_FPS), 1)
        else:
            cap.set(cv2.CAP_PROP_FPS, fps)
        self.fps = fps
        self.cap = cap

class RGBDVideoPlayer(VideoPlayer):
    def get_frame(self):
        self.cap.grab()
        flag1, rgb_img = self.cap.retrieve(flag=cv2.CAP_OPENNI_BGR_IMAGE)
        rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
        flag2, depth_map = self.cap.retrieve(flag=cv2.CAP_OPENNI_DEPTH_MAP)
        if not flag1 or not flag2:
            return

        if rgb_img.shape[:2] != depth_map.shape[:2]:
            imh, imw = depth_map.shape[:2]
            rgb_img = cv2.resize(rgb_img, (imw, imh))

        return rgb_img, depth_map
