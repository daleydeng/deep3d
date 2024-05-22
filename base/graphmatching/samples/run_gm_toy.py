#!/usr/bin/env python
import sys
sys.path.append('../..')
import numpy as np
import h5py
from graphmatching.pbgraphmatching import *
from graphmatching import rrwm

def main(sample_f='sample.h5'):
    fp = h5py.File(sample_f)
    M = np.array(fp['M'])
    GT = np.array(fp['GT'])
    n0, n1 = GT.shape[0], GT.shape[1]
    ms = []
    for i in range(n0):
        for j in range(n1):
            ms.append([n0, n1])

    X_raw, X_sol = rrwm.run_rrwm(M, ms)
    score = X_sol.T.dot(M).dot(X_sol)
    print (np.where(X_sol))
    print (np.where(GT)[1])
    raise
    gm_matches = [matches[i] for i in match_idxs]

    if True:
        matches1to2 = []
        for i, j, d in gm_matches:
            matches1to2.append(cv2.DMatch(i, j, d))

        query_kps = [cv2.KeyPoint(i[0], i[1], 1) for i in query_kps]
        tpl_kps = [cv2.KeyPoint(i[0], i[1], 1) for i in tpl_kps]
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
