import numpy as np

def get_mat(fname):
    with open(fname) as f:
        n = int(f.readline())
        return np.loadtxt(f).reshape(n, n)

try:
    a, b, res = get_mat("matrixA.txt"), get_mat("matrixB.txt"), get_mat("result.txt")
    if np.allclose(res, a @ b, atol=1e-3):
        print("OK: Results are correct!")
    else:
        print("ERROR: Calculations mismatch.")
except Exception as e:
    print(f"Run error: {e}")
