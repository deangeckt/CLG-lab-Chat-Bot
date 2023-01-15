import numpy as np

def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

def dtw_distance(gt, pred):
    gt = np.array([(g['r'], g['c']) for g in gt])
    pred = np.array([(p['r'], p['c']) for p in pred])

    n = len(gt)
    m = len(pred)
    DTW = np.zeros((n+1, m+1))
    for i in range(1, n+1):
        for j in range(1, m+1):
            dist = euclidean_distance(gt[i-1], pred[j-1])
            DTW[i, j] = dist + min(DTW[i-1, j], DTW[i, j-1], DTW[i-1, j-1])
    return DTW[n, m]
