import os
import wx
import wx.media

from recognition_service import *
from microphone_service import *

from application import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class RecognitionSimplePanel(wx.Panel):

    def __init__(self, parent, next_panel, recognition_service_settings, patient_testing_model):
        wx.Panel.__init__(self, parent=parent)

        self.frame = parent
        self.layoutControls()
        self.next_panel = next_panel
        self.recognition_service_settings = recognition_service_settings

        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

        self.hideRecordCircle()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        self.recordBtn = wx.ToggleButton(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать запись", size=(120, 30))
        self.recordBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onRecord)

        self.textRes = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP,
            value="", name="Результаты распознавания", size=(400, 500))

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Продолжить", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.helpLabel = wx.StaticText(self, label="Для того чтобы начать распознавать голос, " \
                                        "нажмите на кнопку 'Начать запись', говорите фразы в микрофон, " \
                                        "а затем нажмите на кнопку еще раз. Распознанный текст выведется " \
                                        "в текстовое поле через 1-10 секунд.", size=(400, 90))

        self.textLabel = wx.StaticText(self, label="Распознанный текст")

        self.redCircle = wx.StaticBitmap(self, bitmap=wx.Bitmap("../libs/scripts/bitmaps/circle.png", wx.BITMAP_TYPE_PNG), size=(32, 32))

        self.recordLabel = wx.StaticText(self, label="Идет запись")

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vvSizer = wx.BoxSizer(wx.VERTICAL)

        self.vvSizer.Add(self.recordBtn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.vvSizer.Add(self.redCircle, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.vvSizer.Add(self.recordLabel, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        self.hSizer.Add(self.vvSizer, 0, wx.ALL, 5)
        self.hSizer.Add(self.helpLabel, 0, wx.ALL, 5)

        self.vSizer.Add(self.hSizer, 0, wx.ALL, 5)
        self.vSizer.Add(self.textLabel, 0, wx.ALL, 5)
        self.vSizer.Add(self.nextBtn, 0, wx.ALL, 5)
        self.vSizer.Add(self.textRes, 0, wx.ALL, 5)
        self.mainSizer.Add(self.vSizer)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def hideRecordCircle(self):
        self.redCircle.Hide()
        self.recordLabel.Hide()
        self.Layout()

    def showRecordCircle(self):
        self.redCircle.Show()
        self.recordLabel.Show()
        self.Layout()

    def startRecord(self):
        self.recording_data = RecordingData()
        start_recording(self.recording_data, self.recognition_service_settings)
        self.showRecordCircle()
        print("Start recording")

    def stopRecord(self):
        wav_file_with_speech = stop_recording(self.recording_data, self.recognition_service_settings)
        self.hideRecordCircle()
        print("Stop Recording")

        text = recognize_wav_file(wav_file_with_speech,
                                  self.recognition_service_settings.recognize_service_url)

        print("Result : {}".format(text))

        self.textRes.Clear()
        if text is None:
            self.textRes.write("< Произошла ошибка, подробности в консоли >")
        else:
            self.textRes.write(text)


    def onRecord(self, event):
        if self.recordBtn.GetValue() == True:
            self.recordBtn.SetLabel("Остановить запись")
            self.startRecord()

        else:
            self.recordBtn.SetLabel("Начать запись")
            self.recordBtn.Disable()
            self.stopRecord()
            self.recordBtn.Enable()

    def nextPanel(self, event):
        if self.next_panel == None:
            return
        
        self.Hide()
        self.next_panel.Show()
        self.Layout()
