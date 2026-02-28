import numpy as np


def detect_active_region(db, threshold_db=20):
    """
    Finds the active sound region based on RMS dB.

    start = first window above (max_db - threshold)
    end   = last window above (max_db - threshold)
    """

    max_db = np.max(db)

    threshold = max_db - threshold_db

    indices = np.where(db > threshold)[0]

    if len(indices) == 0:
        return 0, len(db)

    start = indices[0]
    end = indices[-1]

    return start, end