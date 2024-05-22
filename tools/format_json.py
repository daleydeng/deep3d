#!/usr/bin/env python
import json
def main(json_f):
    d = json.load(open(json_f))
    print (json.dumps(d, sort_keys=True, indent=2, separators=(',', ': ')))

if __name__ == "__main__":
    import fire
    fire.Fire(main)
