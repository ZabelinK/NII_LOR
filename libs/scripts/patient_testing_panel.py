import os
import wx
import wx.media

import patient_testing_model
from patient_testing_model import *
from recognition_service import *
from microphone_service import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PatientTestingPanel(wx.Panel):

    def __init__(self, parent, testing_model, test_settings, recognition_service_setting):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model
        self.test_settings = test_settings
        self.recognition_service_setting = recognition_service_setting

        self.current_testing_item = 0

        self.frame = parent
        self.SetSize((800, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        self.fileLabel = wx.StaticText(self, label="")

        self.playBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Прослушать", size=(120, 30))
        self.playBtn.Bind(wx.EVT_BUTTON, self.onPlay)

        self.playLabel = wx.StaticText(self, label="Звучит запись")

        self.recordBtn = wx.ToggleButton(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать запись", size=(120, 30))
        self.recordBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onRecord)

#        self.redCircle = wx.StaticBitmap(self, bitmap=wx.Bitmap("../libs/scripts/bitmaps/circle.png", wx.BITMAP_TYPE_PNG), size=(32, 32))
        self.recordLabel = wx.StaticText(self, label="Идет запись")

        self.textLabel = wx.StaticText(self, label="Распознанный текст")
        self.textRes = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP,
            value="", name="Результаты распознавания", size=(300, 100))


        self.nextRecBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Следующая запись", size=(120, 30))
        self.nextRecBtn.Bind(wx.EVT_BUTTON, self.nextRecord)

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Показать результаты", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)


        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
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


    def onPlay(self, event):
        pass

    def onRecord(self, event):
        pass

    def nextRecord(self, event):
        pass

    def nextPanel(self, event):
        print("Testing Model content {}".format(self.testing_model))

        self.Hide()
        next(self.parent.current_panel).Show()
        self.Layout()