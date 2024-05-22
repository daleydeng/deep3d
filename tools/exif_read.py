#!/usr/bin/env python
from os import path
from math import radians, tan
from exiftool import ExifTool

INCH = 25.4

def file_name(f):
    return path.basename(path.splitext(f)[0])

# partialy from snavely extract_focal.pl
ccd_width_db = {
    'Nokia N80': 5.27, # 1/2.7
    'Nokia N86 8MP' : 5.27, # 1/2.7 guessed
    'Nokia N93': 4.536, # 1/3.1
    'Nokia N95': 5.7, # 1/2.7
    'Nokia N95 8GB': 5.7, # 1/2.7
    'Nokia N97': 5.7, # guessed
    'Nokia N900': 5.76, # 1/2.5 guessed
    'NIKON CORPORATION NIKON D70s': 23.7,
    'NIKON CORPORATION NIKON D300': 23.7,
    'NIKON COOLPIX S4': 5.76,
    'Canon Canon EOS 450D': 22.2,
    'SONY NEX-5T': 23.7,
}

FPR_UNIT_TP = 2 # inches
INCH = 25.4

def exif_read_focals(fnames, guess_fl):
    if type(guess_fl) == str and path.exists(guess_fl):
        raise
    else:
        guess_focal_db = None

    with ExifTool() as et:
        Ks = {}
        for i, fname in enumerate(fnames):
            if i > 0 and i % 100 == 0:
                print('processing', i)
            mt = et.get_metadata(fname)
            model = mt['EXIF:Make']+' '+mt['EXIF:Model']
            w, h = mt['File:ImageWidth'], mt['File:ImageHeight']
            cam_name = model+'_{}x{}'.format(w, h)
            cam_name = cam_name.replace(' ', '_')
            if w < h:
                w, h = h, w

            if 'EXIF:FocalLength' not in mt:
                if not guess_fl:
                    continue

                if guess_fl == 'max_wh':
                    fx = max(w, h)

                elif guess_fl.startswith('fov'):
                    fov = float(guess_fl[3:])
                    fx = w/2/tan(radians(fov/2))
                elif guess_focal_db:
                    fx = guess_focal_db[file_name(fname)]
                else:
                    raise
                print(fname, 'no focal, guess:', guess_fl, fx)
            else:
                fl = mt['EXIF:FocalLength']
                if 'EXIF:FocalPlaneXResolution' in mt:
                    fpxr = mt['EXIF:FocalPlaneXResolution']
                    fpyr = mt['EXIF:FocalPlaneYResolution']
                    assert mt['EXIF:FocalPlaneResolutionUnit'] == FPR_UNIT_TP
                    w0, h0 = mt['EXIF:ExifImageWidth'], mt['EXIF:ExifImageHeight']
                    assert w0 > h0
                    k = fl * w/w0 /INCH
                    fx = k * fpxr
                    fy = k * fpyr
                elif model in ccd_width_db:
                    ccdw = ccd_width_db[model]
                    fx = w / ccdw * fl
                else:
                    print(fname, model, 'no focal skip')
                    continue

            Ks[file_name(fname)] = {'name': cam_name+'_{}'.format(round(fx, 2)), 'w': mt['File:ImageWidth'], 'h': mt['File:ImageHeight'], 'tp': 'K1', 'd': [round(fx/max(w,h), 6)]}
        return Ks

if __name__ == "__main__":
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('names', nargs='+')
    ap.add_argument('--guess_fl')
    ap.add_argument('-o', default='-')
    args = ap.parse_args()

    assert args.o
    Ks = exif_read_focals(args.names, args.guess_fl)
    print (Ks)
