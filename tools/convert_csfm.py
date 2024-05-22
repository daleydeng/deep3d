#!/usr/bin/env python
from geometry.csfm import load_csfm, save_csfm

def main(src_f, dst_f):
    d = load_csfm(src_f)
    save_csfm(d, dst_f)

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
