#!/usr/bin/env python
import sys
import math
import numpy as np

def _select_dc(N, max_dis, min_dis, distances, auto=False, q=2):
    if auto:
        return _autoselect_dc(N, max_dis, min_dis, distances)
    dc = np.percentile([i for i in distances.values() if i > 0], q)
    return dc

def _autoselect_dc(N, max_dis, min_dis, distances):
    dc = (max_dis + min_dis) / 2
    dists = list(distances.values())
    while True:
        nneighs = sum([1 for v in dists if v < dc]) / N ** 2
        if nneighs >= 0.01 and nneighs <= 0.02:
            break
        # binary search
        if nneighs < 0.01:
            min_dis = dc
        else:
            max_dis = dc
        dc = (max_dis + min_dis) / 2
        if max_dis - min_dis < 0.0001:
            break
    return dc

def _local_density(N, distances, dc, fn='gauss'):
    if fn == 'gauss':
        func = lambda dij, dc: math.exp(- (dij / dc) ** 2)
    elif fn == 'cutoff':
        func = lambda dij, dc: 1 if dij < dc else 0
    else:
        raise

    rho = [0] * N
    for (i, j), d in distances.items():
        d = func(d, dc)
        rho[i] += d
        rho[j] += d
    return np.asarray(rho)

def _min_distance(N, max_dis, distances, rho):
    sorted_rho_idxs = np.argsort(-rho)
    delta, nneigh = [max_dis] * len(rho), [-1] * len(rho)
    max_rho_id = sorted_rho_idxs[0]
    delta[max_rho_id] = 0.

    for i in range(1, N):
        ii = sorted_rho_idxs[i]
        for j in range(i):
            jj = sorted_rho_idxs[j]
            d = distances[min(ii, jj), max(ii, jj)]
            if d < delta[ii]:
                delta[ii] = d
                nneigh[ii] = jj
        delta[max_rho_id] = max(delta[ii], delta[max_rho_id])

    return delta, nneigh, sorted_rho_idxs

def _decide_centers(rho, delta, nr_meth='gap', win_size=2, ratio=0.8):
    rd = rho*delta
    sorted_idxs = np.argsort(-rd)
    if nr_meth == 'gap':
        gaps = [-1]
        log_rd = sorted(np.log(rd), reverse=True)
        for i in range(1, len(log_rd)):
            gap = np.mean(log_rd[:i]) - log_rd[i]
            if gap < gaps[max(i-win_size, 0)]:
                break
            else:
                gaps.append(gap)
        cluster_nr = np.argmax(gaps)
    elif nr_meth == 'ratio':
        max_v = rd[sorted_idxs[0]]
        for idx, i in enumerate(sorted_idxs):
            if rd[i] < max_v * ratio:
                break
        cluster_nr = idx

    elif type(nr_meth) == int:
        cluster_nr = nr_meth
    else:
        raise

    labels = [-1]*len(rd)
    center_idxs = sorted_idxs[:cluster_nr]
    for idx, i in enumerate(center_idxs):
        labels[i] = idx
    return labels, center_idxs

def run_cluster(distances, cluster_nr_meth='gap', dc='auto', density_fn='gauss'):
    max_dis = max(distances.values())
    min_dis = min(distances.values())
    ids = set()
    for i, j in distances.keys():
        ids.add(i)
        ids.add(j)
    ids = sorted(ids)
    N = ids[-1]+1

    if dc in ('auto', 'manual'):
        dc = _select_dc(N, max_dis, min_dis,
                       distances, auto=(dc == 'auto'))

    rho = _local_density(N, distances, dc, fn=density_fn)
    delta, nneigh, sorted_rho_idxs = _min_distance(N, max_dis, distances, rho)
    print (rho < 0.5*dc)

    labels, center_idxs = _decide_centers(rho, delta, nr_meth=cluster_nr_meth)
    for i in sorted_rho_idxs:
        if labels[i] < 0:
            labels[i] = labels[nneigh[i]]

    return labels, center_idxs
