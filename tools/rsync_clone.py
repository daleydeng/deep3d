#!/usr/bin/env python
import os
from os import path
from tempfile import mkstemp

def dirnames(f):
    out = []
    while True:
        f = path.dirname(f)
        if not f or f == '/':
            break
        out.append(f)
    return reversed(out)

def fix_rules_file(rules_f):
    appends = []
    contents = []
    for l in open(rules_f):
        prefix, p = l.split()
        if prefix == '+':
            for d in dirnames(p):
                if d not in contents:
                    contents.append(d)
        contents.append(prefix+' '+p)

    tmp_f = mkstemp('.rules', 'rsync')[-1]
    with open(tmp_f, 'w') as fp:
        for l in contents:
            print (l, file=fp)

    return tmp_f

cmd_tpl = 'rsync {test} -m --recursive -L -av {delete} --include-from={rules_f} {src} {dst}'
def main(src, rules_f, dst, delete=False, t=True):
    src = src+'/'
    if delete:
        delete = '--delete'
    else:
        delete = ''

    tmp_rules_f = fix_rules_file(rules_f)

    cmd = cmd_tpl.format(src=src, rules_f=tmp_rules_f, dst=dst, delete=delete, test=("--dry-run" if t else ""))
    print (cmd)
    os.system(cmd)
    os.remove(tmp_rules_f)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
