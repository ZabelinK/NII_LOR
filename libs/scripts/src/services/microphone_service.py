import numpy as np
import sounddevice as sd
import soundfile as sf


class RecordingData:
    data = np.empty([1, 2])
    stream = 'null'


def start_recording(recording_data, recognition_service_settings):
    def callback(indata, frames, time, status):
        recording_data.data = np.append(recording_data.data, indata, axis=0)

    recording_data.stream = sd.InputStream(samplerate=recognition_service_settings.fs, channels=2, callback=callback)
    recording_data.stream.start()


def stop_recording(file_name, recording_data, recognition_service_settings):
    recording_data.stream.stop()
    return save_data_to_wav_file(file_name, recording_data, recognition_service_settings)


def save_data_to_wav_file(file_name, recording_data, recognition_service_settings):
    file_name = recognition_service_settings.temp_dir + file_name
    sf.write(file_name,
             recording_data.data,
             recognition_service_settings.fs)
    return file_name