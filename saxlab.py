import os
import time
from datetime import datetime

import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf

from util import detect_active_region


# ===============================
# CONFIG
# ===============================

DURATION = 10
SR = 44100

FMIN = 200
FMAX = 1200

WINDOW_MS = 50
ACTIVE_DB_THRESHOLD = 20

STABLE_FREQ_THRESHOLD = 20  # Hz


# ===============================
# RECORD
# ===============================

def countdown(seconds=3):
    print("\nPrepare...")
    for i in range(seconds, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("GO!\n")


def record_audio(duration, sr):

    print("Recording:")

    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)

    for i in range(duration):
        print(f"  {i+1}/{duration} sec")
        time.sleep(1)

    sd.wait()

    print("Done recording\n")

    return audio.flatten()


# ===============================
# SIGNAL PROCESSING
# ===============================

def compute_rms_db(audio, sr, window_ms):

    window_size = int(sr * window_ms / 1000)

    rms_values = []

    for i in range(0, len(audio) - window_size, window_size):

        window = audio[i:i+window_size]

        rms = np.sqrt(np.mean(window**2))

        db = 20 * np.log10(rms + 1e-9)

        rms_values.append(db)

    return np.array(rms_values)


def pitch_to_cents(f0):

    mean_freq = np.nanmean(f0)

    cents = 1200 * np.log2(f0 / mean_freq)

    return cents


# ===============================
# ANALYSIS
# ===============================

def analyze(audio):

    f0, voiced_flag, _ = librosa.pyin(
        audio,
        fmin=FMIN,
        fmax=FMAX,
        sr=SR
    )

    db = compute_rms_db(audio, SR, WINDOW_MS)

    # detect active tone region
    start_w, end_w = detect_active_region(db, ACTIVE_DB_THRESHOLD)

    # convert window index to frame index
    frames_per_window = len(f0) / len(db)

    start_f = int(start_w * frames_per_window)
    end_f = int(end_w * frames_per_window)

    f0_active = f0[start_f:end_f]
    db_active = db[start_w:end_w]

    # pitch stats
    mean_freq = np.nanmean(f0_active)
    std_freq = np.nanstd(f0_active)

    cents = pitch_to_cents(f0_active)

    std_cents = np.nanstd(cents)

    # dB stats
    mean_db = np.mean(db_active)
    std_db = np.std(db_active)

    # stable tone duration
    stable_mask = np.abs(f0_active - mean_freq) < STABLE_FREQ_THRESHOLD

    frame_duration = len(audio)/SR / len(f0)

    stable_duration = np.sum(stable_mask) * frame_duration

    return {
        "f0": f0,
        "db": db,
        "cents": cents,
        "mean_freq": mean_freq,
        "std_freq": std_freq,
        "std_cents": std_cents,
        "mean_db": mean_db,
        "std_db": std_db,
        "stable_duration": stable_duration,
        "start_w": start_w,
        "end_w": end_w,
        "start_f": start_f,
        "end_f": end_f
    }


# ===============================
# PLOTS
# ===============================

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

    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)

    plt.figure(figsize=(10,4))

    plt.title("Spectrogram")

    librosa.display.specshow(D, y_axis='log', x_axis='time')

    plt.colorbar(format='%+2.0f dB')

    plt.savefig(path)

    plt.close()


# ===============================
# FILE SYSTEM
# ===============================

def create_run_dir():

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = os.path.join("runs", ts)

    os.makedirs(run_dir, exist_ok=True)

    return run_dir


def save_stats(stats, path):

    with open(path, "w") as f:

        f.write("SAXLAB RESULTS\n\n")

        f.write(f"Mean frequency: {stats['mean_freq']:.2f} Hz\n")
        f.write(f"Std frequency: {stats['std_freq']:.2f} Hz\n")
        f.write(f"Pitch stability: {stats['std_cents']:.2f} cents\n\n")

        f.write(f"Mean dB (RMS): {stats['mean_db']:.2f}\n")
        f.write(f"Std dB (RMS): {stats['std_db']:.2f}\n\n")

        f.write(f"Stable tone duration: {stats['stable_duration']:.2f} sec\n")


# ===============================
# MAIN
# ===============================

def main():

    run_dir = create_run_dir()

    countdown()

    audio = record_audio(DURATION, SR)

    sf.write(os.path.join(run_dir, "audio.wav"), audio, SR)

    stats = analyze(audio)

    plot_pitch(stats["f0"], stats["start_f"], stats["end_f"], os.path.join(run_dir, "pitch.png"))

    plot_cents(stats["cents"], os.path.join(run_dir, "cents.png"))

    plot_db(stats["db"], stats["start_w"], stats["end_w"], os.path.join(run_dir, "db.png"))

    plot_spectrogram(audio, os.path.join(run_dir, "spectrogram.png"))

    save_stats(stats, os.path.join(run_dir, "stats.txt"))

    print("=== RESULTS ===\n")

    print(f"Mean frequency: {stats['mean_freq']:.2f} Hz")
    print(f"Std frequency: {stats['std_freq']:.2f} Hz")
    print(f"Pitch stability: {stats['std_cents']:.2f} cents")

    print()

    print(f"Mean dB (RMS): {stats['mean_db']:.2f}")
    print(f"Std dB (RMS): {stats['std_db']:.2f}")

    print()

    print(f"Stable tone duration: {stats['stable_duration']:.2f} sec")

    print(f"\nSaved to: {run_dir}")


if __name__ == "__main__":
    main()