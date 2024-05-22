import cv2
from pyfbow.pbfbow import *

class ImageSearch:
    def __init__(self, feature_nr=500):
        self.voc = Vocabulary()
        voc.readFile(environ['DEEP3D_BASE']+'/data/fbow/orb_mur.fbow')
        self.orb = cv2.ORB_create(feature_nr)
        self.

    def add_images(self, imgs):
        vvs = []
        for i in imgs:
            kps, descs = orb.detectAndCompute(i, None)
            vvs.append(voc.tansform(descs))
