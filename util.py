import numpy as np

def trim_attack(f0):

    f0_clean = f0[~np.isnan(f0)]

    median = np.median(f0_clean)

    for i in range(len(f0)):

        if abs(f0[i] - median) < 15:
            return f0[i:]

    return f0