import os
import wx
import wx.media

from services.recognition_service import *
from services.microphone_service import *
from services.sound_service import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, '../../bitmaps')


class PatientAutoTestingPanel(wx.Panel):

    def __init__(self, parent, testing_model, test_settings, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model
        self.test_settings = test_settings
        self.recognition_service_settings = recognition_service_settings

        self.current_testing_item = 0

        self.frame = parent
        self.SetSize((800, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        self.fioLabel = wx.StaticText(self, label="{} {}".format("ФИО: ",
                                                                 self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel = wx.StaticText(self, label="{} {}".format("Год рождения: ", self.testing_model.birthday))
        self.fileLabel = wx.StaticText(self, label="", size=(400, 30))
        self.playRecLabel = wx.StaticText(self, label="", size=(400, 30))
        self.countdownLabel = wx.StaticText(self, label="", size=(400, 30))

        self.textLabel = wx.StaticText(self, label="Распознанный текст")
        self.textRes = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                   value="", name="Результаты распознавания", size=(300, 100))
        self.textRes.Bind(wx.EVT_TEXT, self.onKeyTyped)

        self.startBtn = wx.Button(self, style=wx.SL_VERTICAL | wx.SL_INVERSE, label="Начать сессию", size=(120, 30))
        self.startBtn.Bind(wx.EVT_BUTTON, self.startSession)

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL | wx.SL_INVERSE, label="Показать результаты", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.fioLabel)
        self.mainSizer.Add(self.birthdayLabel)
        self.mainSizer.Add(self.fileLabel, 0, wx.ALL, 5)
        self.mainSizer.Add(self.playRecLabel, 0, wx.ALL, 5)
        self.mainSizer.Add(self.countdownLabel, 0, wx.ALL, 5)
        self.mainSizer.Add(self.textLabel, 0, wx.ALL, 5)
        self.mainSizer.Add(self.textRes, 0, wx.ALL, 5)

        self.hSizerBtn = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerBtn.Add(self.startBtn, 0, wx.ALL, 5)
        self.hSizerBtn.Add(self.nextBtn, 0, wx.ALL, 5)

        self.mainSizer.Add(self.hSizerBtn, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.Layout()

        self.nextBtn.Disable()

    def update(self):
        self.fioLabel.SetLabel(
            "{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel.SetLabel("{} {}".format("Год рождения: ", self.testing_model.birthday))
        if self.current_testing_item < self.test_settings.audioFilesNumber:
            test_item = self.testing_model.testingItems[self.current_testing_item]
            index = str(self.current_testing_item + 1) + " из " + str(self.test_settings.audioFilesNumber) + ":  "
            self.fileLabel.SetLabel(index + test_item.initialAudioFilePath)
        else:
            self.fileLabel.SetLabel("Все файлы кончились")
            self.nextBtn.Enable()

    def play(self):
        self.update()
        test_item = self.testing_model.testingItems[self.current_testing_item]

        self.textRes.Clear()
        self.playRecLabel.SetLabel("Воспроизведение")
        noise_file = self.recognition_service_settings.noises_dir + self.test_settings.noiseFile \
            if self.test_settings.noiseFile != '' \
            else None
        play_file( self.recognition_service_settings.words_dir + test_item.initialAudioFilePath,self.test_settings.volumeLevelNoice, noise_file)

    def onKeyTyped(self, event):
        test_item = self.testing_model.testingItems[self.current_testing_item]
        test_item.resultAudioFilePath = test_item.initialAudioFilePath
        test_item.resultTest = event.GetString().lower()
        test_item.isCorrect = test_item.initialText == test_item.resultTest

    def record(self):
        self.startRecord()
        self.playRecLabel.SetLabel("Запись")
        delay_time = self.test_settings.delay * 1000    # getting delay in milliseconds
        count = 0
        while count < delay_time:
            count += 250
            self.countdownLabel.SetLabel(self.get_countdown_text(delay_time, count))
            wx.MilliSleep(250)
        self.stopRecord()
        wx.MilliSleep(250)

    def get_countdown_text(self, total_time, left_time):
        left_ticks = 16
        right_ticks = 16
        mid_ticks = 5
        total_ticks = left_ticks + right_ticks + mid_ticks
        full_sym = '+'
        empty_sym = '~'
        edge_sym = '!'
        ticks = int(left_time / total_time * total_ticks)
        left_line = edge_sym
        right_line = ""
        if ticks <= left_ticks:
            left_line += full_sym * ticks + empty_sym * (left_ticks - ticks)
            right_line = empty_sym * right_ticks + edge_sym
        elif ticks > left_ticks + mid_ticks:
            left_line += full_sym * left_ticks
            right_line = (ticks - (left_ticks + mid_ticks)) * full_sym + empty_sym * (total_ticks - ticks) + edge_sym
        else:
            left_line += full_sym * left_ticks
            right_line = empty_sym * right_ticks + edge_sym
        minutes = (total_time - left_time) // 60000
        if minutes < 10:
            minutes = "0" + str(minutes)
        else:
            minutes = str(minutes)
        seconds = ((total_time - left_time) // 1000) % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)
        return left_line + " " + minutes + ":" + seconds + " " + right_line

    def startRecord(self):
        self.playRecLabel.SetLabel("Запись")
        self.recording_data = RecordingData()
        start_recording(self.recording_data, self.recognition_service_settings)
        print("Start recording")

    def stopRecord(self):
        self.update()
        test_item = self.testing_model.testingItems[self.current_testing_item]
        test_item.resultAudioFilePath = test_item.initialAudioFilePath
        wav_file_with_speech = stop_recording(test_item.resultAudioFilePath, self.recording_data,
                                              self.recognition_service_settings)
        self.playRecLabel.SetLabel("Распознавание")
        print("Stop Recording")

        # TODO: UNCOMMENT WHEN RECOGNITION SERVICE WILL BE STABLE
        # text = recognize_wav_file(wav_file_with_speech,
        #                           self.recognition_service_settings.recognize_service_url)
        text = "Текст заглушка"

        print("Result : {}".format(text))

        self.textRes.Clear()
        if text is None:
            self.textRes.write("< Произошла ошибка, подробности в консоли >")
            return

        self.textRes.write(text)
        test_item.resultTest = text.lower()
        test_item.isCorrect = test_item.initialText == test_item.resultTest
        wx.MilliSleep(1000)

    def nextPanel(self, event):

        print("Testing Model content {}".format(self.testing_model))

        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def startSession(self, event):
        self.startBtn.Disable()

        for i in range(self.test_settings.audioFilesNumber):
            self.current_testing_item = i
            self.play()
            self.record()
            self.update()
        self.playRecLabel.SetLabel("Конец сессии")
        self.nextBtn.Enable()
