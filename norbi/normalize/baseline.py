import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

def baseline_als(y, lam, p, niter=10):
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    D = lam * D.dot(D.transpose()) # Precompute this term since it does not depend on `w`
    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)
    for i in range(niter):
        W.setdiag(w) # Do not create a new matrix, just update diagonal values
        Z = W + D
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z

def baseline_all(df, lam, p, niter=100):

    for i in range(len(df.columns)-1):

        x_val = df.iloc[:,0]
        y_val = df.iloc[:,(i+1)]

        base = baseline_als(y_val, lam, p, niter=100)
        
        df.iloc[:,0] = x_val
        
        df.iloc[:,(i+1)] = y_val-base

    return df