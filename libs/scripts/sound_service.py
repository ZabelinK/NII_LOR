import numpy as np
import sounddevice as sd
import soundfile as sf


def play_file(file_path, noise_path=None):
    data, fs = sf.read(file_path, dtype='float32')

    if noise_path != None:
        noise_data, noise_fs = sf.read(noise_path, dtype='float32')    
        assert noise_fs == fs
        res = 0.5 * data + 0.5 * noise_data[:len(data)] 
    else:
        res = data

    sd.play(res, fs)
    sd.wait()