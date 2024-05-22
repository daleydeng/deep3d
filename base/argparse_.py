import os
from os import path
from glob import glob

def parse_file_list_out(fnames, out=None):
    if len(fnames) == 1:
        if path.isdir(fnames[0]):
            d = fnames[0]
            fnames = [d+'/'+i for i in os.listdir(d)]

    if not out:
        out = path.dirname(fnames[0])
        if not out:
            out = '.'

    os.makedirs(out, exist_ok=True)
    return fnames, out

def parse_size(s):
    return tuple(int(i) for i in s.split('x'))

def parse_files2(f1, f2):
    if path.isdir(f1) and path.isdir(f2):
        fnames = sorted(set(path.splitext(i)[0] for i in os.listdir(f1)) & set(path.splitext(i)[0] for i in os.listdir(f2)))
        f1s = [glob(f1+'/{}*'.format(i))[0] for i in fnames]
        f2s = [glob(f2+'/{}*'.format(i))[0] for i in fnames]
    else:
        f1s = [f1]
        f2s = [f2]
    return f1s, f2s
