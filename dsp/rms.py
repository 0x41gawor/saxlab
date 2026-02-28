import numpy as np


def compute_rms_db(audio, sr, window_ms):

    window_size = int(sr * window_ms / 1000)

    db = []

    for i in range(0, len(audio) - window_size, window_size):

        window = audio[i:i + window_size]

        rms = np.sqrt(np.mean(window ** 2))

        db.append(20 * np.log10(rms + 1e-9))

    return np.array(db)