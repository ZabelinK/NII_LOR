import numpy as np
import sounddevice as sd
import soundfile as sf


def play_file(file_path, noise_path=None):
    #TODO: Implement noise overlapping

    data, fs = sf.read(file_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()