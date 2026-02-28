import numpy as np
import librosa


def estimate_pitch(audio, sr, fmin, fmax):

    f0, _, _ = librosa.pyin(
        audio,
        fmin=fmin,
        fmax=fmax,
        sr=sr
    )

    return f0


def pitch_to_cents(f0):

    mean_freq = np.nanmean(f0)

    cents = 1200 * np.log2(f0 / mean_freq)

    return cents