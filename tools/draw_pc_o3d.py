#!/usr/bin/env python
import open3d as o3d
from pc3d.pc_o3d import *

def main(src_f):
    pc = o3d.io.read_point_cloud(src_f)
    draw_pc(pc)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
