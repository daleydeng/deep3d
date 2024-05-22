import numpy as np
import os
from os import path
from pymatbridge import Matlab
mlab_d = os.environ['DEEP3D_BASE'] + '/contrib/matlab'

class Mlab:
    def __init__(self, *args, **kws):
        self.mlab = Matlab(*args, **kws)
        self.mlab.start()

    def run_func(self, fname, *args, **kws):
        ret = self.mlab.run_func(path.join(mlab_d, fname), *args, **kws)
        print (ret['content']['stdout'])
        if not ret['success']:
            raise
        return ret['result']

def from_midx(i):
    return int(i)-1
