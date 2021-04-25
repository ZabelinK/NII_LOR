class PatientTestingModel:

    def __init__(self):
        self.firstName = ''
        self.middleName = ''
        self.secondName = ''
        self.birthday = ''
        self.testDay = ''
        self.testingItems = []


class TestingItem:

    def __init__(self):
        self.initialAudioFilePath = ''
        self.initialText = ''
        self.resultAudioFilePath = ''
        self.resultTest = ''
        self.isCorrect = ''
        self.commentText = ''


class TestSettings:

    def __init__(self):
        self.audioFilesNumber = ''
        self.noiseFile = ''
        self.volumeLevel = 50


class RecognitionServiceSettings:

    def __init__(self, tempDir):
        self.recognize_service_url = 'https://asr.kube.plintum.dev/recognize?lang=ru'
        self.tempFileName = "out.wav"
        self.fs = 8000
        self.tempDir = tempDir
