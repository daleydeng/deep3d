import numpy as np
from skimage.transform import resize
from queue import Queue
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QColor

def npa_to_QImage(a):
    if a.ndim == 2:
        gray = np.require(a, dtype=np.uint8)
        h, w = gray.shape
        qim = QImage(gray.data, w, h, QImage.Format_Indexed8)
        for i in range(256):
            qim.setColor(i, QColor(i, i, i).rgb())
        return qim

    if a.ndim == 3:
        rgb = np.require(a, dtype=np.uint8)
        h, w, chns = rgb.shape
        return QImage(rgb.data, w, h, QImage.Format_RGB888 if chns == 3 else QImage.Format_RGBA8888)

    raise

def resize_img(img, new_w=-1, new_h=-1, mode=min):
    h, w = img.shape[:2]
    ratio = 1.0
    if new_w > 0:
        ratio = mode(new_w / w, ratio)
    if new_h > 0:
        ratio = mode(new_h / h, ratio)
    if ratio == 1.0:
        return img
    return resize(img, (int(h*ratio), int(w*ratio)), preserve_range=True)


class QueueProcessor(QThread):
    sig_done = pyqtSignal(object, int)
    def __init__(self, max_size=100, *args, **kws):
        super().__init__(*args, **kws)
        self.q = Queue(max_size)

    def put(self, d, id=0):
        self.q.put((d, id))

    def process_one(self, d):
        return d

    def run(self):
        self.is_running = True
        while self.is_running:
            if self.q.empty():
                time.sleep(0.02)
            else:
                while True:
                    o = self.q.get()
                    if o is None:
                        break
                    item, id = o
                    ret = self.process_one(item)
                    self.sig_done.emit(ret, id)
                    self.q.task_done()

    def stop(self):
        self.is_running = False
        self.wait()
