#!/usr/bin/env python
import json

def main(*src_fs, out_f='merged.json', pretty=True):
    d0 = json.load(open(src_fs[0]))
    if type(d0) == list:
        out = []
        tp = 'array'
    elif type(d0) == dict:
        out = {}
        tp = 'dict'

    for src_f in src_fs:
        a = json.load(open(src_f))
        if tp == 'array':
            out += a
        elif tp == 'dict':
            out.update(a)

    kws = {}
    if pretty:
        kws = {
            'sort_keys': True,
            'indent': 2,
            'separators': (',', ': '),
        }
    json.dump(out, open(out_f, 'w'), **kws)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
