import argparse

from config import Config
from audio.recorder import AudioRecorder
from analysis.analyzer import Analyzer

from sessions.single_run import SingleRunSession
from sessions.embochure import EmbouchureSession


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["single", "embouchure"],
        default="single"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Recording duration in seconds (single mode only)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=3,
        help="Seconds between runs (embouchure mode only)"
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=5,
        help="Number of runs (embouchure mode only)"
    )

    args = parser.parse_args()

    cfg = Config()

    recorder = AudioRecorder(cfg.audio.sample_rate)

    analyzer = Analyzer(cfg)

    if args.mode == "single":
        duration = args.duration if args.duration is not None else cfg.audio.duration
        session = SingleRunSession(
            recorder,
            analyzer,
            duration,
            cfg.audio.sample_rate
        )

    else:
        duration = args.duration if args.duration is not None else cfg.audio.duration
        session = EmbouchureSession(
            recorder,
            analyzer,
            duration=duration,
            interval=args.interval,
            repetitions=args.repeat
        )

    session.run()


if __name__ == "__main__":
    main()