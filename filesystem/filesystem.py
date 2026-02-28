# filesystem/filesystem.py

from datetime import datetime
import os
import soundfile as sf


class Filesystem:

    def __init__(self):
        self.path = self.create_run_dir()

    def create_run_dir(self):

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        run_dir = os.path.join("artifacts", "runs", ts)

        os.makedirs(run_dir, exist_ok=True)

        return run_dir

    def artifact(self, name):
        return os.path.join(self.path, name)

    def save_stats(self, stats):

        filename = self.artifact("stats.txt")

        with open(filename, "w") as f:

            f.write("SAXLAB RESULTS\n\n")

            f.write(f"Mean frequency: {stats['mean_freq']:.2f} Hz\n")
            f.write(f"Std frequency: {stats['std_freq']:.2f} Hz\n")
            f.write(f"Pitch stability: {stats['pitch_stability']:.2f} cents\n\n")

            f.write(f"Mean dB (RMS): {stats['mean_db']:.2f}\n")
            f.write(f"Std dB (RMS): {stats['std_db']:.2f}\n\n")

            f.write(f"Stable tone duration: {stats['stable_duration']:.2f} sec\n")

    def save_audio(self, audio, sample_rate):

        sf.write(self.artifact("audio.wav"), audio, sample_rate)