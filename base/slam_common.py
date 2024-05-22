import os
from os import path
import numpy as np
import cv2
from cv2 import VideoCapture, imread, cvtColor

def RC2P(R, C):
    return np.dot(R, np.hstack((np.eye(3), -np.asarray(C)[:,None])))

def concat_trans(T0, T1):
    return np.hstack(T1[:3,:3].dot(T0[:3,:3]), (T1[:3,:3].dot(T0[:3,3]) + T1[:3,3])[:,None])

def listdir(d, fullname=False, sort=False):
    ret = os.listdir(d)
    if sort:
        ret = sorted(ret)
    if fullname:
        ret = [path.join(d, i) for i in ret]
    return ret

def change_path(fname, ext='', d=''):
    n, ext0 = splitext(fname)
    dd, n = path.split(n)
    if not ext:
        ext = ext0
    if d:
        dd = d
    return path.join(dd, n+ext)

class FrameSeq:
    def __init__(self, clip, start_idx=0, end_idx=-1, interval=1, name='{:06d}', use_gray=True):
        tp = type(clip)
        if tp == str and ('%' in clip or path.splitext(clip)[-1].lower() in ('.mp4',)):
            self.clip = VideoCapture(clip)
            assert self.clip.isOpened()
        elif tp == str and path.isdir(clip):
            self.clip = listdir(clip, fullname=True, sort=True)
        elif tp == list:
            # images
            self.clip = clip
        elif tp == VideoCapture:
            self.clip = clip

        tp = type(self.clip)
        if tp == list:
            self.next_frame = self._next_frame_imgseq
        elif 'VideoCapture' in str(tp):
            # Video
            self.next_frame = self._next_frame_cap

        self.cur_idx = -1
        self.name = name
        self.interval = interval
        self.start_idx = start_idx
        self.end_idx = end_idx if end_idx >= 0 else float('inf')
        self.use_gray = use_gray

    def _next_frame_cap(self):
        self.cur_idx += 1
        flag, frame = self.clip.read()
        if self.cur_idx % self.interval != 0 or self.cur_idx < self.start_idx:
            return 'continue', None
        if not flag or self.cur_idx > self.end_idx:
            return 'end', None

        self.cur_fname = self.name.format(self.cur_idx)
        return 'ok', frame

    def _next_frame_imgseq(self):
        self.cur_idx += 1
        if self.cur_idx > len(self.clip)-1:
            return "end", None

        if self.cur_idx % self.interval != 0 or self.cur_idx < self.start_idx:
            return 'continue', None
        if self.cur_idx > self.end_idx:
            return 'end', None

        frame = self.clip[self.cur_idx]
        self.cur_fname = self.name.format(self.cur_idx)
        if type(frame) == str:
            self.cur_fname = frame
            frame = imread(frame)
        return 'ok', frame

    def each_frame(self):
        while True:
            flag, frame = self.next_frame()
            if flag == 'end':
                break
            if flag == 'continue':
                continue
            if self.use_gray:
                if frame.ndim == 3:
                    gray = cvtColor(frame, cv2.COLOR_RGB2GRAY)
                else:
                    gray = frame
                yield gray, frame, self.cur_idx-self.start_idx, self.cur_fname
            else:
                yield frame, self.cur_idx-self.start_idx, self.cur_fname
