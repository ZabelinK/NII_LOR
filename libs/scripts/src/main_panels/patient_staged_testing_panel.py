import os
import wx
import wx.media

from services.recognition_service import *
from services.microphone_service import *
from services.sound_service import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, '../../bitmaps')


class PatientStagedTestingPanel(wx.Panel):

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

        self.title = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_title = wx.StaticText(self, -1, "Шаг 4. Тестирование пациента")
        self.fioLabel = wx.StaticText(self, label="{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.middleName + " " + self.testing_model.secondName))
        self.birthdayLabel = wx.StaticText(self, label="{} {}".format("Год рождения: ", self.testing_model.birthday))

        self.fileLabel = wx.StaticText(self, label="")

        self.playBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Прослушать", size=(120, 30))
        self.playBtn.Bind(wx.EVT_BUTTON, self.onPlay)

        self.playLabel = wx.StaticText(self, label="Звучит запись")

        self.recordBtn = wx.ToggleButton(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать запись", size=(120, 30))
        self.recordBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onRecord)

#        self.redCircle = wx.StaticBitmap(self, bitmap=wx.Bitmap("../libs/scripts/bitmaps/circle.png", wx.BITMAP_TYPE_PNG), size=(32, 32))
        self.recordLabel = wx.StaticText(self, label="Идет запись")

        self.textLabel = wx.StaticText(self, label="Распознанный текст")
        self.textRes = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_WORDWRAP,
            value="", name="Результаты распознавания", size=(300, 100))
        self.textRes.Bind(wx.EVT_TEXT, self.onKeyTyped)

        self.nextRecBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Следующая запись", size=(120, 30))
        self.nextRecBtn.Bind(wx.EVT_BUTTON, self.nextRecord)

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Показать результаты", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)


        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.title.Add(self.panel_title, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.mainSizer.Add(self.title)
        self.mainSizer.Add(self.fioLabel)
        self.mainSizer.Add(self.birthdayLabel)
        self.mainSizer.Add(self.fileLabel, 0, wx.ALL, 5)

        self.vSizerPlay = wx.BoxSizer(wx.VERTICAL)
        self.vSizerPlay.Add(self.playBtn, 0, wx.ALL, 5)
        self.vSizerPlay.Add(self.playLabel, 0, wx.ALL, 5)

        self.vSizerRec = wx.BoxSizer(wx.VERTICAL)
        self.vSizerRec.Add(self.recordBtn, 0, wx.ALL, 5)
        self.vSizerRec.Add(self.recordLabel, 0, wx.ALL, 5)

        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer.Add(self.vSizerPlay, 0, wx.ALL, 5)
        self.hSizer.Add(self.vSizerRec, 0, wx.ALL, 5)

        self.mainSizer.Add(self.hSizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.textLabel, 0, wx.ALL, 5)
        self.mainSizer.Add(self.textRes, 0, wx.ALL, 5)

        self.hSizerBtn = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerBtn.Add(self.nextRecBtn, 0, wx.ALL, 5)
        self.hSizerBtn.Add(self.nextBtn, 0, wx.ALL, 5)

        self.mainSizer.Add(self.hSizerBtn, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.Layout()

        self.playLabel.Hide()
        self.recordLabel.Hide()
    
    def update(self):
        self.fioLabel.SetLabel("{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel.SetLabel("{} {}".format("Год рождения: ", self.testing_model.birthday))
        self.textRes.Clear()
        if self.current_testing_item < self.test_settings.audioFilesNumber:
            test_item = self.testing_model.testingItems[self.current_testing_item]
            self.fileLabel.SetLabel(test_item.initialAudioFilePath)
        else:
            self.fileLabel.SetLabel("Все файлы кончились")
            self.playBtn.Disable()
            self.nextRecBtn.Disable()
            self.recordBtn.Disable()

    def onPlay(self, event):
        self.playBtn.Disable()
        test_item = self.testing_model.testingItems[self.current_testing_item]
        self.currentVolumeNoice = self.test_settings.volumeLevelNoice
        self.playLabel.Show()
        noise_file = self.recognition_service_settings.noises_dir + self.test_settings.noiseFile \
                        if self.test_settings.noiseFile != '' \
                        else None
        play_file( self.recognition_service_settings.words_dir + test_item.initialAudioFilePath,self.test_settings.volumeLevelNoice, noise_file)
        self.playLabel.Hide()
        self.playBtn.Enable()

    def onKeyTyped(self, event):
        test_item = self.testing_model.testingItems[self.current_testing_item]
        test_item.resultAudioFilePath = test_item.initialAudioFilePath
        test_item.resultTest = event.GetString().lower()
        test_item.isCorrect = test_item.initialText == test_item.resultTest

    def onRecord(self, event):
        if self.recordBtn.GetValue() == True:
            self.recordBtn.SetLabel("Остановить запись")
            self.playBtn.Disable()
            self.nextBtn.Disable()
            self.nextRecBtn.Disable()
            self.startRecord()
        else:
            self.recordBtn.Disable()
            self.stopRecord()
            self.recordBtn.SetLabel("Начать запись")
            self.recordBtn.Enable()
            self.playBtn.Enable()
            self.nextBtn.Enable()
            self.nextRecBtn.Enable()
        
    def nextRecord(self, event):
        self.current_testing_item += 1
        self.update()

    def startRecord(self):
        self.recordLabel.Show()
        self.recording_data = RecordingData()
        start_recording(self.recording_data, self.recognition_service_settings)
        #self.showRecordCircle()
        print("Start recording")
 
    def stopRecord(self):
        test_item = self.testing_model.testingItems[self.current_testing_item]
        test_item.resultAudioFilePath = test_item.initialAudioFilePath
        wav_file_with_speech = stop_recording(test_item.resultAudioFilePath, self.recording_data, self.recognition_service_settings)
        self.recordLabel.Hide()
        print("Stop Recording")

        text = recognize_wav_file(wav_file_with_speech,
                                  self.recognition_service_settings.recognize_service_url)

        print("Result : {}".format(text))

        self.textRes.Clear()
        if text is None:
            self.textRes.write("< Произошла ошибка, подробности в консоли >")
            return
 
        self.textRes.write(text)
        test_item.resultTest = text.lower()
        test_item.isCorrect = test_item.initialText == test_item.resultTest


    def nextPanel(self, event):
        print("Testing Model content {}".format(self.testing_model))

        self.Hide()
        next(self.parent.current_panel)
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()