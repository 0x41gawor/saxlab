import time
import numpy as np

from sessions.single_run import SingleRunSession


class EmbouchureSession:

    def __init__(self, recorder, analyzer, duration, interval, repetitions):

        self.recorder = recorder
        self.analyzer = analyzer

        self.interval = interval
        self.duration = duration
        self.repetitions = repetitions

    def run(self):

        results = []
        next_countdown = 3

        for i in range(self.repetitions):

            print(f"\nRun {i+1}/{self.repetitions}")

            run_start = time.monotonic()
            session = SingleRunSession(
                self.recorder,
                self.analyzer,
                self.duration,
                self.recorder.sr
            )
            stats = session.run(countdown_seconds=next_countdown)

            results.append(stats)

            elapsed = time.monotonic() - run_start
            remaining = self.interval - elapsed
            next_countdown = max(0, remaining)

        summary = self._summarize(results)
        self._print_summary(summary)

        return {
            "runs": results,
            "summary": summary
        }

    def _summarize(self, results):
        summary = {}
        keys = [
            "mean_freq",
            "std_freq",
            "std_cents",
            "mean_db",
            "std_db",
            "stable_duration"
        ]

        for key in keys:
            values = np.array([r[key] for r in results], dtype=float)
            summary[key] = {
                "mean": float(np.mean(values)),
                "std": float(np.std(values))
            }

        summary["pitch_stability"] = summary["std_cents"]

        return summary

    def _print_summary(self, summary):
        print("\n=== SUMMARY ===\n")

        print(
            "Mean frequency: "
            f"{summary['mean_freq']['mean']:.2f} Hz "
            f"(std: {summary['mean_freq']['std']:.2f})"
        )
        print(
            "Std frequency: "
            f"{summary['std_freq']['mean']:.2f} Hz "
            f"(std: {summary['std_freq']['std']:.2f})"
        )
        print(
            "Pitch stability: "
            f"{summary['pitch_stability']['mean']:.2f} cents "
            f"(std: {summary['pitch_stability']['std']:.2f})"
        )

        print()

        print(
            "Mean dB (RMS): "
            f"{summary['mean_db']['mean']:.2f} "
            f"(std: {summary['mean_db']['std']:.2f})"
        )
        print(
            "Std dB (RMS): "
            f"{summary['std_db']['mean']:.2f} "
            f"(std: {summary['std_db']['std']:.2f})"
        )

        print()

        print(
            "Stable tone duration: "
            f"{summary['stable_duration']['mean']:.2f} sec "
            f"(std: {summary['stable_duration']['std']:.2f})"
        )