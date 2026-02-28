from dataclasses import dataclass


@dataclass
class AudioConfig:
    sample_rate: int = 44100
    duration: int = 10


@dataclass
class DSPConfig:
    fmin: int = 200
    fmax: int = 1200
    window_ms: int = 50
    active_db_threshold: int = 20
    stable_freq_threshold: int = 20


@dataclass
class PlotConfig:
    figsize = (10,4)

@dataclass
class Config:
    audio = AudioConfig()
    dsp = DSPConfig()