import os
import time
from datetime import datetime

import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf


# ===============================
# CONFIG
# ===============================

DURATION = 10
SR = 44100

FMIN = 200
FMAX = 1200

WINDOW_MS = 50
GATE_DB = 25

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


def apply_gate(db_values, gate_db):

    max_db = np.max(db_values)

    mask = db_values > (max_db - gate_db)

    return mask


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

    # RMS dB

    db = compute_rms_db(audio, SR, WINDOW_MS)

    gate_mask = apply_gate(db, GATE_DB)

    db_voiced = db[gate_mask]

    # pitch stats

    mean_freq = np.nanmean(f0)
    std_freq = np.nanstd(f0)

    cents = pitch_to_cents(f0)

    std_cents = np.nanstd(cents)

    # dB stats

    mean_db = np.mean(db_voiced)
    std_db = np.std(db_voiced)

    # stable tone duration

    stable_mask = np.abs(f0 - mean_freq) < STABLE_FREQ_THRESHOLD

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
        "stable_duration": stable_duration
    }


# ===============================
# PLOTS
# ===============================

def plot_pitch(f0, path):

    plt.figure(figsize=(10,4))

    plt.title("Pitch (Hz)")

    plt.plot(f0)

    plt.ylabel("Hz")
    plt.xlabel("frame")

    plt.savefig(path)

    plt.close()


def plot_cents(cents, path):

    plt.figure(figsize=(10,4))

    plt.title("Pitch deviation (cents)")

    plt.plot(cents)

    plt.axhline(0)

    plt.ylabel("cents")
    plt.xlabel("frame")

    plt.savefig(path)

    plt.close()


def plot_db(db, path):

    plt.figure(figsize=(10,4))

    plt.title("Amplitude RMS (dB)")

    plt.plot(db)

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

    plot_pitch(stats["f0"], os.path.join(run_dir, "pitch.png"))

    plot_cents(stats["cents"], os.path.join(run_dir, "cents.png"))

    plot_db(stats["db"], os.path.join(run_dir, "db.png"))

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