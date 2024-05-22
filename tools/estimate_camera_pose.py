#!/usr/bin/env python
import numpy as np
import yaml
from pprint import pprint
from geometry.common import decompose_projection, Rt_center
from geometry.geography import ll2xz
from geometry.ransac import ransac_fns
from pyp3pf.common import ransac_p3pf

def main(matches_f, o=None, th=0.01, fmt='xyz', tp='p3pf', params={}):
    out_f = o
    fmt = []
    gvars = {}
    ms = []
    ll0 = None
    for l in open(matches_f):
        if l[0] == '#' and not fmt:
            fmt = l[1:].split()
            for idx, f in enumerate(fmt):
                if ':' in f:
                    k, v = f.split(':')
                    if k in ('imw', 'imh'):
                        gvars[k] = int(v)
            imw, imh = gvars['imw'], gvars['imh']
            cx = imw/2
            cy = imh/2
            continue
        if l[0] == '#':
            continue
        parts = {fmt[idx]: float(i) if fmt[idx] != 'id' else i for idx, i in enumerate(l.split())}
        if all(i in parts for i in 'XYZ'):
            X = [parts['X'], parts['Y'], parts['Z']]
        elif all(i in parts for i in ['lat', 'lng', 'h']):
            ll = parts['lat'], parts['lng']
            if ll0 is None:
                ll0 = ll
            xx, zz = ll2xz(ll, ll0)
            yy = -parts['h']
            X = [xx, yy, zz]

        u = [(parts['u']-cx)/imw, (parts['v']-cy)/imw]
        ms.append([X, u])

    kws = {}
    if tp == 'p3pf':
        if 'focal_lengths' in params:
            kws['focal_lengths'] = params['focal_lengths']
        if 'focal_probs' in params:
            kws['focal_probs'] = params['focal_probs']

    elif tp == 'p5pfr':
        kws['rd_nr'] = params.get('rd_nr', 1)
    else:
        raise

    if tp == 'p3pf':
        ret = ransac_p3pf(ms, th=th, **kws)
    else:
        ret = ransac_fns[tp](ms, th=th, **kws)

    if not ret:
        print ("no result")
        exit()
    P, summary = ret
    if tp in ('p4pf', 'p3pf'):
        K, P = decompose_projection(P)
        fl = float(K[0,0])
    elif tp == 'p5pfr':
        P, fl, r = P
    else:
        raise

    fl = fl * imw
    out = {
        'solver': tp,
        'imw': imw,
        'imh': imh,
        'K': [[fl, 0, cx], [0, fl, cy], [0,0,1]],
        'P': P.tolist(),
        't': Rt_center(P).tolist(),
        'inl_nr': len(summary.inliers),
        'ms_nr': len(ms),
        'inls': summary.inliers,
        'iter_nr': summary.iter_nr,
    }
    if tp == 'p5pfr':
        out['rd'] = r
    pprint (out)
    if out_f:
        yaml.dump(out, open(out_f, 'w'))

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
