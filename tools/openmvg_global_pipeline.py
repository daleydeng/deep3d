#!/usr/bin/env python
import os
import subprocess
import sys
import json

def run_cmd(s):
    print ('cmd:', s)
    p = subprocess.Popen(s.split())
    p.wait()

def main(img_d='images', out_d='out', recon_d='recon', matches_d='matches', tp='global'):
    sensor_db_f = sys.exec_prefix+'/share/openMVG/sensor_width_camera_database.txt'

    assert tp in ('global', 'inc')
    recon_d = out_d+'/'+recon_d+'_'+tp
    matches_d = out_d + '/'+matches_d

    os.makedirs(out_d, exist_ok=True)
    os.makedirs(recon_d, exist_ok=True)
    os.makedirs(matches_d, exist_ok=True)

    print (tp, img_d, out_d)
    print ("1. Intrinsics analysis")
    run_cmd("openMVG_main_SfMInit_ImageListing -i {} -o {} -d {}".format(img_d, matches_d, sensor_db_f))

    print ("2. Compute features")
    run_cmd("openMVG_main_ComputeFeatures -i {0}/sfm_data.json -o {0} -m SIFT".format(matches_d))

    print ("3. Compute matches")
    if tp == 'global':
        run_cmd("openMVG_main_ComputeMatches -i {0}/sfm_data.json -o {0} -ge".format(matches_d))
    else:
        run_cmd("openMVG_main_ComputeMatches -i {0}/sfm_data.json -o {0}".format(matches_d))

    print ("4. Do reconstruction")
    if tp == 'global':
        cmd = 'GlobalSfM'
    else:
        cmd = 'IncrementalSfM'
    run_cmd("openMVG_main_{cmd} -i {0}/sfm_data.json -m {0} -o {1}".format(matches_d, recon_d, cmd=cmd))

    run_cmd("openMVG_main_ComputeSfM_DataColor -i {0}/sfm_data.bin -o {0}/colorized.ply".format(recon_d))

    print ("6. Structure from Known Poses (robust triangulation)")
    m_f = matches_d+'/matches.e.bin'
    if not os.path.exists(m_f):
        m_f = matches_d+'/matches.f.bin'

    run_cmd("openMVG_main_ComputeStructureFromKnownPoses -i {0}/sfm_data.bin -m {1} -f {m_f} -o {0}/robust.bin".format(recon_d, matches_d, m_f=m_f))
    run_cmd("openMVG_main_ComputeSfM_DataColor -i {0}/robust.bin -o  {0}/robust_colorized.ply".format(recon_d))

    run_cmd('openMVG_main_ConvertSfM_DataFormat -i {0}/sfm_data.bin -o {0}/sfm_data.json'.format(recon_d))
    run_cmd('openMVG_main_ConvertSfM_DataFormat -i {0}/robust.bin -o {0}/robust.json'.format(recon_d))

    print ("7. export undistorted")
    run_cmd('openMVG_main_ExportUndistortedImages -i {0}/sfm_data.json -o {0}/ud_images -r 1'.format(recon_d))

    for name in ['sfm_data', 'robust']:
        sfm_data = json.load(open(recon_d+'/'+name+'.json'))
        sfm_data['ud_img_path'] = recon_d+'/ud_images'
        for i in sfm_data['intrinsics']:
            v = i['value']
            d = v['ptr_wrapper']['data']
            del v['polymorphic_name']
            del v['polymorphic_id']
            del d['disto_k3']

        json.dump(sfm_data, open(recon_d+'/'+name+'_ud.json', 'w'), indent=2)

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
