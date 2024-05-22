#!/usr/bin/env python
import os

def main(list_f, dst_d='.'):
    os.makedirs(dst_d, exist_ok=True)
    for l in open(list_f):
        parts = l.split()
        if not parts or l[0] == '#':
            continue
        if len(parts) == 2 and parts[-1][-1] != '/':
            url, to = parts
            out_f = dst_d + '/'+to
            out_dir = os.path.dirname(out_f)
            if out_dir != dst_d:
                os.makedirs(out_dir, exist_ok=True)
            cmd = 'wget -nc '+url+' -O '+out_f
        else:
            url = parts[0]
            if len(parts) == 2:
                out_d = dst_d+'/'+parts[-1]
            else:
                out_d = dst_d
            cmd = 'wget -nc '+url+' -P '+out_d
        os.system(cmd)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
