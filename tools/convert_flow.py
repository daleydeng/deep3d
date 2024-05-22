#!/usr/bin/env python
import numpy as np
import os
from imgproc.common import load_flow

def main(src, dst_f=None):
    if not dst_f:
        dst_f = os.path.splitext(src)[0]+'.npy'
    data = load_flow(src)
    np.save(dst_f, data)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
