import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

class Plotter:
    def __init__(self, audio, stats, fs):
        self.stats = stats
        self.fs = fs
        self.audio = audio
    
    def run(self):
        plot_pitch(
            self.stats["f0"],
            self.stats["start_f"],
            self.stats["end_f"],
            self.fs.artifact("pitch.png")
        )

        plot_cents(
            self.stats["cents"],
            self.fs.artifact("cents.png")
        )

        plot_db(
            self.stats["db"],
            self.stats["start_w"],
            self.stats["end_w"],
            self.fs.artifact("db.png")
        )

        plot_spectrogram(
            self.audio,
            self.fs.artifact("spectrogram.png")
        )




def plot_pitch(f0, start_f, end_f, path):

    plt.figure(figsize=(10,4))

    plt.title("Pitch (Hz)")

    plt.plot(f0)

    plt.axvline(start_f, color="red")
    plt.axvline(end_f, color="red")

    plt.ylabel("Hz")
    plt.xlabel("frame")

    plt.savefig(path)

    plt.close()


def plot_cents(cents, path):

    plt.figure(figsize=(10,4))

    plt.title("Pitch deviation (cents)")

    plt.plot(cents)

    plt.axhline(0)
    plt.axhline(20, linestyle=":")
    plt.axhline(-20, linestyle=":")

    plt.ylabel("cents")
    plt.xlabel("frame")

    plt.savefig(path)

    plt.close()


def plot_db(db, start_w, end_w, path):

    plt.figure(figsize=(10,4))

    plt.title("Amplitude RMS (dB)")

    plt.plot(db)

    plt.axvline(start_w, color="red")
    plt.axvline(end_w, color="red")

    plt.ylabel("dB")
    plt.xlabel("window")

    plt.savefig(path)

    plt.close()


def plot_spectrogram(audio, path):

    D = librosa.amplitude_to_db(
        np.abs(librosa.stft(audio)),
        ref=np.max
    )

    plt.figure(figsize=(10,4))

    plt.title("Spectrogram")

    librosa.display.specshow(
        D,
        y_axis='log',
        x_axis='time'
    )

    plt.colorbar(format='%+2.0f dB')

    plt.savefig(path)

    plt.close()