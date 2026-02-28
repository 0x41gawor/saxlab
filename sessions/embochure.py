class EmbouchureSession:

    def __init__(self, recorder, analyzer, interval, measure_time, repetitions):

        self.recorder = recorder
        self.analyzer = analyzer

        self.interval = interval
        self.measure_time = measure_time
        self.repetitions = repetitions

    def run(self):

        results = []

        for i in range(self.repetitions):

            print(f"\nRun {i+1}/{self.repetitions}")

            audio = self.recorder.record(self.measure_time)

            stats = self.analyzer.analyze(audio)

            results.append(stats)

            print(stats)

            time.sleep(self.interval)

        return results