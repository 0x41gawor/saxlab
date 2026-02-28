import numpy as np

from dsp import pitch
from dsp import rms
from dsp import onset


class Analyzer:

    def __init__(self, config):
        self.cfg = config

    def analyze(self, audio):

        sr = self.cfg.audio.sample_rate

        # pitch estimation
        f0 = pitch.estimate_pitch(
            audio,
            sr,
            self.cfg.dsp.fmin,
            self.cfg.dsp.fmax
        )

        # RMS dB
        db = rms.compute_rms_db(
            audio,
            sr,
            self.cfg.dsp.window_ms
        )

        # detect active sound region
        start_w, end_w = onset.detect_active_region(
            db,
            self.cfg.dsp.active_db_threshold
        )

        # convert window index → pitch frame index
        frames_per_window = len(f0) / len(db)

        start_f = int(start_w * frames_per_window)
        end_f = int(end_w * frames_per_window)

        # active regions
        f0_active = f0[start_f:end_f]
        db_active = db[start_w:end_w]

        # pitch statistics
        mean_freq = np.nanmean(f0_active)
        std_freq = np.nanstd(f0_active)

        cents = pitch.pitch_to_cents(f0_active)
        std_cents = np.nanstd(cents)

        # dB statistics
        mean_db = np.mean(db_active)
        std_db = np.std(db_active)

        # stable tone duration
        stable_mask = np.abs(f0_active - mean_freq) < self.cfg.dsp.stable_freq_threshold

        frame_duration = len(audio) / sr / len(f0)

        stable_duration = np.sum(stable_mask) * frame_duration

        return {
            # raw signals
            "f0": f0,
            "db": db,
            "cents": cents,

            # pitch stats
            "mean_freq": mean_freq,
            "std_freq": std_freq,
            "std_cents": std_cents,

            # alias (for future refactor compatibility)
            "pitch_stability": std_cents,

            # loudness stats
            "mean_db": mean_db,
            "std_db": std_db,

            # duration
            "stable_duration": stable_duration,

            # region indices
            "start_w": start_w,
            "end_w": end_w,
            "start_f": start_f,
            "end_f": end_f
        }   