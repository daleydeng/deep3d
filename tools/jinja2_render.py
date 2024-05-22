#!/usr/bin/env python
from jinja2 import Template

def main(src_f):
    tpl = Template(open(src_f).read())
    print (tpl.render())

if __name__ == "__main__":
    import fire
    fire.Fire(main)
