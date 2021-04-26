from utils import *
from constants import DEFAULT_WORK_DIR
from constants import PATH_TO_WORDS
from constants import PATH_TO_NOISES
from constants import PATH_TO_BITMAPS
from constants import PATH_TO_DOCS_TEMPALTES

class PatientTestingModel:

    def __init__(self):
        self.firstName = ''
        self.middleName = ''
        self.secondName = ''
        self.birthday = ''
        self.testDay = ''
        self.testingItems = []

    def __repr__(self):
        return obj_to_str(self)


class TestingItem:

    def __init__(self):
        self.initialAudioFilePath = ''
        self.initialText = ''
        self.resultAudioFilePath = ''
        self.resultTest = ''
        self.isCorrect = ''
        self.commentText = ''

    def __repr__(self):
        return obj_to_str(self)


class TestSettings:

    def __init__(self):
        self.audioFilesNumber = 0
        self.noiseFile = ''
        self.volumeLevel = 50

    def __repr__(self):
        return obj_to_str(self)


class RecognitionServiceSettings:

    def __init__(self, temp_dir, input_dir, words_dir, noises_dir, bitmaps_dir, template_dir):
        self.recognize_service_url = 'https://asr.kube.plintum.dev/recognize?lang=ru'
        self.tempFileName = "out.wav"
        self.fs = 8000
        if temp_dir:
            self.temp_dir = temp_dir
        else:
            self.temp_dir = DEFAULT_WORK_DIR

        if input_dir:
            self.input_dir = input_dir
        else:
            self.input_dir = PATH_TO_WORDS

        if words_dir:
            self.words_dir = words_dir
        else:
            self.words_dir = PATH_TO_WORDS

        if noises_dir:
            self.noises_dir = noises_dir
        else:
            self.noises_dir = PATH_TO_NOISES

        if bitmaps_dir:
            self.bitmaps_dir = bitmaps_dir
        else:
            self.bitmaps_dir = PATH_TO_BITMAPS

        if template_dir:
            self.template_dir = template_dir
        else:
            self.template_dir = PATH_TO_DOCS_TEMPALTES