import numpy as np
from .pbgraphmatching import bistoc_norm

def _make_group1(ids):
    unique_ids = sorted(set(ids))
    grp = np.zeros((len(ids), len(unique_ids)), dtype=bool)
    for i, unique_id in enumerate(unique_ids):
        grp[ids==unique_id,i] = True
    return grp

def _make_group12(ms):
    ms = np.asarray(ms)
    return _make_group1(ms[:,0]), _make_group1(ms[:,1])

def _get_conflict_mat(grp1, grp2):
    grp = np.hstack((grp1, grp2))
    nr = grp.shape[0]
    cmat = np.zeros((nr, nr))
    rows, cols = grp.nonzero()
    for j in cols:
        rows = grp[:,j].nonzero()[0]
        for i in rows:
            cmat[i, rows] = 1
    np.fill_diagonal(cmat, 0)
    return cmat

def _make_groups(grp):
    rows, cols = grp.nonzero()
    ID, idx = zip(*sorted(zip(cols, rows)))
    return np.array(idx), np.array(ID)

def _make_groups_slack(idx1, ID1, idx2, ID2):
    grp1_nr, grp2_nr = ID1[-1]+1, ID2[-1]+1
    dum_val = int(grp2_nr - grp1_nr)
    dum_size = grp2_nr
    max_idx = len(idx1)
    add_idx = list(range(max_idx, max_idx+grp2_nr))
    idx1 = np.concatenate((idx1, add_idx))
    ID1 = np.concatenate((ID1, grp1_nr*np.ones(grp2_nr)))

    add_ID = list(range(grp2_nr))
    tmp_idx = np.zeros(max_idx+grp2_nr)
    tmp_ID = np.zeros_like(tmp_idx)

    i = 0
    j = 0
    while i < max_idx - 1:
        tmp_idx[i+j], tmp_ID[i+j] = idx2[i], ID2[i]
        if ID2[i] != ID2[i+1]:
            tmp_idx[i+j+1], tmp_ID[i+j+1] = add_idx[j], add_ID[j]
            j += 1
        i += 1

    while i < max_idx:
        tmp_idx[i+j], tmp_ID[i+j] = idx2[i], ID2[i]
        if i == max_idx-1:
            tmp_idx[i+j+1], tmp_ID[i+j+1] = add_idx[j], add_ID[j]
            j += 1
        i += 1

    idx2, ID2 = tmp_idx, tmp_ID
    return idx1, ID1, idx2, ID2, dum_val, dum_size

def _greedy_mapping(score, grp1, grp2):
    score = score.copy()
    Xd = np.zeros(len(score))
    max_v, max_idx = score.max(), score.argmax()
    while max_v > 0:
        Xd[max_idx] = 1
        grp1_idx = grp1[max_idx,:].nonzero()[0]
        score[grp1[:,grp1_idx].nonzero()[0]] = 0
        grp2_idx = grp2[max_idx,:].nonzero()[0]
        score[grp2[:,grp2_idx].nonzero()[0]] = 0
        max_v, max_idx = score.max(), score.argmax()
    return Xd

# tol is the convergence th for the Sinkhorn method
def run_rrwm(M, matches, c=0.2, amp_max=30, max_iters=300,
             convergence_th=1e-25, tol=1e-3, mapping='greedy'):
    grp1, grp2 = _make_group12(matches)
    idx1, ID1 = _make_groups(grp1)
    idx2, ID2 = _make_groups(grp2)
    if ID1[-1] < ID2[-1]:
        idx1, ID1, idx2, ID2, dum_val, dum_size = _make_groups_slack(
            idx1, ID1, idx2, ID2)
        dum_dim = 1
    elif ID1[-1] > ID2[-1]:
        idx2, ID2, idx1, ID1, dum_val, dum_size = _make_groups_slack(
            idx2, ID2, idx1, ID1)
        dum_dim = 2
    else:
        dum_dim, dum_val, dum_size = 0, 0, 0

    M = M * (_get_conflict_mat(grp1, grp2) == 0)
    d = np.sum(M, axis=1)
    Mo = M / max(d)
    ms_nr = len(M)
    prev_score = np.ones(ms_nr) / ms_nr
    prev_score2 = prev_score
    prev_assign = np.ones(ms_nr) / ms_nr

    for iter_i in range(max_iters):
        cur_score = Mo.dot(c * prev_score + (1-c)*prev_assign)
        s = sum(cur_score)
        if s > 0:
            cur_score /= s

        cur_assign = cur_score
        amp_value = amp_max / max(cur_assign)
        cur_assign = np.exp(amp_value * cur_assign)

        X_slack = np.concatenate((cur_assign, dum_val * np.ones(dum_size)))
        X_slack = bistoc_norm(X_slack, idx1, ID1, idx2, ID2, tol, dum_dim, dum_val, 1000)
        cur_assign = X_slack[:ms_nr]
        s = sum(cur_assign)
        if s > 0:
            cur_assign /= s

        diff1 = sum((cur_score - prev_score)**2)
        diff2 = sum((cur_score - prev_score2)**2)
        diff_min = min(diff1, diff2)
        if diff_min < convergence_th:
            break

        prev_score2 = prev_score
        prev_score = cur_score
        prev_assign = cur_assign

    if mapping == 'greedy':
        return cur_score, _greedy_mapping(cur_score, grp1, grp2)
    else:
        return cur_score
