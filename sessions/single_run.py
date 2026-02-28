import time

from filesystem.filesystem import Filesystem

from plots.plotter import Plotter


class SingleRunSession:

    def __init__(self, recorder, analyzer, duration, sample_rate):

        self.recorder = recorder
        self.analyzer = analyzer
        self.duration = duration
        self.sample_rate = sample_rate

    def run(self):

        fs = Filesystem()

        countdown()

        audio = self.recorder.record(self.duration)

        fs.save_audio(audio, self.sample_rate)

        stats = self.analyzer.analyze(audio)

        print("=== RESULTS ===\n")

        print(f"Mean frequency: {stats['mean_freq']:.2f} Hz")
        print(f"Std frequency: {stats['std_freq']:.2f} Hz")
        print(f"Pitch stability: {stats['pitch_stability']:.2f} cents")

        print()

        print(f"Mean dB (RMS): {stats['mean_db']:.2f}")
        print(f"Std dB (RMS): {stats['std_db']:.2f}")

        print()

        print(f"Stable tone duration: {stats['stable_duration']:.2f} sec")

        plt = Plotter(audio, stats,fs)
        plt.run()
        fs.save_stats(stats)
        print(f"\nSaved to: {fs.path}")

        return stats


def countdown(seconds=3):
        print("\nPrepare...")
        for i in range(seconds, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("GO!\n")