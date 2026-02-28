import numpy as np


def detect_active_region(db, threshold_db):

    max_db = np.max(db)

    threshold = max_db - threshold_db

    indices = np.where(db > threshold)[0]

    if len(indices) == 0:
        return 0, len(db)

    return indices[0], indices[-1]