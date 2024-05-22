#!/usr/bin/env python
import os.path as osp
import yaml
import pickle

def main(src_f, dst_f=None):
    d = yaml.load(open(src_f))
    if not dst_f:
        dst_f = osp.splitext(src_f)[0]+'.pkl'
    pickle.dump(d, open(dst_f, 'wb'))

if __name__ == "__main__":
    import fire
    fire.Fire(main)
