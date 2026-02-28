import sounddevice as sd
import time


class AudioRecorder:

    def __init__(self, sample_rate):
        self.sr = sample_rate

    def record(self, duration):
        
        print(f"\nRecording: ")
        audio = sd.rec(
            int(duration * self.sr),
            samplerate=self.sr,
            channels=1
        )

        for i in range(duration):
            print(f"  {i+1}/{duration} sec")
            time.sleep(1)

        sd.wait()

        print("Done recording\n")

        return audio.flatten()