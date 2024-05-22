import numpy as np
import numpy.linalg as npl
import cv2
from cv2 import optflow

class Flow:
    def __init__(self):
        self.op = optflow.createOptFlow_DIS(optflow.DISOPTICAL_FLOW_PRESET_ULTRAFAST)

    def flow_consistency(self, gray0, gray1, mag_th=0.01):
        assert gray0.shape == gray1.shape
        tot_nr = np.prod(gray0.shape[:2])
        mag_th *= max(gray0.shape[:2])
        forward_flow = self.op.calc(gray0, gray1, None)
        backward_flow = self.op.calc(gray1, gray0, None)
        diff_mag = npl.norm(forward_flow - backward_flow, axis=-1)
        consistent_nr = (diff_mag < mag_th).sum()
        return consistent_nr/tot_nr
