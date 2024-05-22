#!/usr/bin/env python
import sys
sys.path.append('../..')
import signal; signal.signal(signal.SIGINT, signal.SIG_DFL)
import numpy as np
import numpy.linalg as npl
from annoy import AnnoyIndex
import cv2
from pyvlfeat import *
from graphmatching.pbgraphmatching import *
from graphmatching import rrwm

def draw_keypoints(canvas, kps):
    for kp in kps:
        x, y = kp.pt
        x, y = int(x), int(y)
        cv2.circle(canvas, (x, y), int(kp.size), color=(0,0,255), thickness=3)

def distmat2affinity(distmat, th):
    affinity = th - distmat
    affinity[affinity < 0] = 0
    np.fill_diagonal(affinity, 0)
    return affinity

def read_features(fname, root_sift=True):
    fp = open(fname)
    dim = int(fp.readline())
    N = int(fp.readline())
    kps = []
    feats = []
    for i in range(N):
        parts = fp.readline().split()
        kps.append([float(i) for i in parts[:5]])
        feats.append([int(i) for i in parts[5:]])
    feats = np.array(feats, dtype='f4')
    if root_sift:
        feats = to_root_sift(feats)
    return np.array(kps), feats

def hesaff_to_aff(d):
    N = len(d)
    affs = np.zeros((N, 9))
    affs[:, -1] = 1
    affs[:, 2] = d[:, 0]
    affs[:, 5] = d[:, 1]

    A = d[:,2]**0.5
    B = d[:,3] / A

    affs[:, 0] = A
    affs[:, 1] = B
    affs[:, 3] = 0
    affs[:, 4] = (d[:,4] - B**2)**0.5
    return affs

def frame_to_aff(d):
    N = len(d)
    affs = np.zeros((N, 9))
    affs[:, -1] = 1
    affs[:, [2,5]] = d[:, [0,1]]
    affs[:, [0,1]] = d[:, [2,3]]
    affs[:, [3,4]] = d[:, [4,5]]
    return affs

def to_root_sift(descs):
    den = np.maximum(npl.norm(descs, axis=1, keepdims=True), 1e-6)
    return (descs / den)**0.5

def extract_features(img):
    covdet = CovDet(VlCovDetMethod.VL_COVDET_METHOD_DOG)
    frames = covdet.compute_features(img)
    descs = covdet.extract_descriptors()
    descs = to_root_sift(descs)
    return frames, descs

def main(tpl_f, query_f, feat_nr=-1, lowe_ratio=0.7):
    tpl_img = cv2.imread(tpl_f)
    tpl_frames, tpl_descs = extract_features(tpl_img)
    query_img = cv2.imread(query_f)
    query_frames, query_descs = extract_features(query_img)
    index = AnnoyIndex(128, metric='angular')
    for i, f in enumerate(tpl_descs):
        index.add_item(i, f)

    index.build(10)

    matches = []
    for idx, f in enumerate(query_descs):
        nns, dists = index.get_nns_by_vector(f, 2, include_distances=True)
        if dists[0] / dists[1] < lowe_ratio:
            matches.append([idx, nns[0], dists[0]])

    tpl_affs = frame_to_aff(tpl_frames)
    query_affs = frame_to_aff(query_frames)

    m_query_affs = np.array([query_affs[m[0]] for m in matches])
    m_tpl_affs = np.array([tpl_affs[m[1]] for m in matches])
    M = get_distmat_affine_ste(m_query_affs, m_tpl_affs)
    A = distmat2affinity(M, 10)

    gm_in_matches = [[m[0], m[1]] for m in matches]
    X_raw, X_sol = rrwm.run_rrwm(A, gm_in_matches)
    score = X_sol.T.dot(A).dot(X_sol)
    match_idxs = X_sol.nonzero()[0]
    gm_matches = [matches[i] for i in match_idxs]

    if True:
        matches1to2 = []
        for i, j, d in gm_matches:
            matches1to2.append(cv2.DMatch(i, j, d))

        query_kps = [cv2.KeyPoint(i[2], i[5], 1) for i in query_affs]
        tpl_kps = [cv2.KeyPoint(i[2], i[5], 1) for i in tpl_affs]
        canvas = cv2.drawMatches(query_img, query_kps, tpl_img, tpl_kps, matches1to2, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        #cv2.imwrite("gm_matches.jpg", canvas)
        cv2.imshow("gm_match", canvas)
        cv2.waitKey(-1)
        # matches1to2 = []
        # for i, j, d in matches:
        #     matches1to2.append(cv2.DMatch(i, j, d))

        # canvas = cv2.drawMatches(query_img, query_kps, tpl_img, tpl_kps, matches1to2, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        # cv2.imwrite("matches.jpg", canvas)

    # A = feats.dot(feats.T)
    # np.fill_diagonal(A, 0)
    # A = A.max() - A
    # db = DBSCAN(eps=0.04, min_samples=2, metric='precomputed').fit(A)
    # labels = db.labels_
    # cluster_nr = labels.max()+1

    # for cluster_idx in range(cluster_nr):
    #     word = list(np.where(labels == cluster_idx)[0])
    #     print (len(word))
    #     canvas = img.copy()
    #     draw_keypoints(canvas, [kps[i] for i in word])
    #     cv2.imshow('test', canvas)
    #     cv2.waitKey(-1)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
