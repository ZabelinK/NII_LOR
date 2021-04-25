from utils import *

class PatientTestingModel:

    def __init__(self):
        self.firstName = ''
        self.middleName = ''
        self.secondName = ''
        self.birthday = ''
        self.testDay = ''
        self.testingItems = []
        self.testingSettings = TestSettings()

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

    def __init__(self, tempDir):
        self.recognize_service_url = 'https://asr.kube.plintum.dev/recognize?lang=ru'
        self.tempFileName = "out.wav"
        self.fs = 8000
        self.tempDir = tempDir
