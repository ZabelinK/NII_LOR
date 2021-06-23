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
        self.fileLabel = wx.StaticText(self, label="")
        self.playRecLabel = wx.StaticText(self, label="Звучит запись")

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
        self.mainSizer.Add(self.textLabel, 0, wx.ALL, 5)
        self.mainSizer.Add(self.textRes, 0, wx.ALL, 5)

        self.hSizerBtn = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerBtn.Add(self.startBtn, 0, wx.ALL, 5)
        self.hSizerBtn.Add(self.nextBtn, 0, wx.ALL, 5)

        self.mainSizer.Add(self.hSizerBtn, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.Layout()

        # self.nextBtn.Disable() TODO: UNCOMMENT!
        self.playRecLabel.Hide()

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

        self.playRecLabel.SetLabel("Воспроизведение")
        self.playRecLabel.Show()
        noise_file = self.recognition_service_settings.noises_dir + self.test_settings.noiseFile \
            if self.test_settings.noiseFile != '' \
            else None
        play_file( self.recognition_service_settings.words_dir + test_item.initialAudioFilePath,self.test_settings.volumeLevelNoice, noise_file)
        self.playRecLabel.Hide()

    def onKeyTyped(self, event):
        test_item = self.testing_model.testingItems[self.current_testing_item]
        test_item.resultAudioFilePath = test_item.initialAudioFilePath
        test_item.resultTest = event.GetString().lower()
        test_item.isCorrect = test_item.initialText == test_item.resultTest

    def record(self):
        self.startRecord()

        delay_time = self.test_settings.delay * 4
        dlg = wx.ProgressDialog("Запись",
                                "Идёт запись",
                                maximum=delay_time,
                                parent=self,
                                style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_REMAINING_TIME
                                )
        keepGoing = True
        count = 0
        while keepGoing and count < delay_time:
            count += 1
            wx.MilliSleep(250)
            (keepGoing, skip) = dlg.Update(count)
        dlg.Update(delay_time)
        dlg.Hide()
        dlg.Destroy()
        wx.MilliSleep(250)
        self.stopRecord()

    # def nextRecord(self):
    #     self.current_testing_item += 1
    #     self.update()

    def startRecord(self):
        self.playRecLabel.SetLabel("Запись")
        self.playRecLabel.Show()
        self.recording_data = RecordingData()
        start_recording(self.recording_data, self.recognition_service_settings)
        # self.showRecordCircle()
        print("Start recording")

    def stopRecord(self):
        self.update()
        test_item = self.testing_model.testingItems[self.current_testing_item]
        test_item.resultAudioFilePath = test_item.initialAudioFilePath
        wav_file_with_speech = stop_recording(test_item.resultAudioFilePath, self.recording_data,
                                              self.recognition_service_settings)
        self.playRecLabel.Hide()
        print("Stop Recording")

        # TODO: UNCOMMENT WHEN DEBUG END
        # text = recognize_wav_file(wav_file_with_speech,
        #                           self.recognition_service_settings.recognize_service_url)
        text = "Заглушечный тЭкст"

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
