import os
import wx
import wx.media
import wx.grid

from patient_testing_model import *
from recognition_service import *
from microphone_service import *

from sound_service import *
from constants import *

import wx.lib.scrolledpanel as scrolled

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')



class PatientResultPanel(scrolled.ScrolledPanel):

    def __init__(self, parent, testing_model, test_settings, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model
        self.test_settings = test_settings
        self.recognition_service_settings = recognition_service_settings

        self.SetSize((1200, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def update(self):

        self.SetSize((1200, 600))
        self.grid = wx.GridSizer(self.test_settings.audioFilesNumber, 5, 5, 5)

        self.all_check_box = []
        self.count = 0
        self.btn_to_file = {}
        btn_count = 0
        noise_path = None
        if self.test_settings.noiseFile:
            noise_path = PATH_TO_NOISES + self.test_settings.noiseFile

        for item in self.testing_model.testingItems:
            labelCorrect = wx.StaticText(self, label=item.initialText)
            playOrigBtn = wx.Button(self, id=btn_count, style=wx.SL_INVERSE, label="Play", size=(100, 30))
            playOrigBtn.Bind(wx.EVT_BUTTON, self.playRecord)
            labelRecord = wx.StaticText(self, label=item.resultTest)

            self.btn_to_file[btn_count] = PATH_TO_WORDS + item.initialAudioFilePath
            btn_count +=1

            playRecBtn = wx.Button(self, id=btn_count, style=wx.SL_INVERSE, label="Play", size=(100, 30))
            playRecBtn.Bind(wx.EVT_BUTTON, self.playRecord)
            
            self.btn_to_file[btn_count] = self.recognition_service_settings.tempDir + item.resultAudioFilePath
            btn_count +=1

            checkBox = wx.CheckBox(self)
            checkBox.Bind(wx.EVT_CHECKBOX, self.updateCheckBox)

            if item.isCorrect:
                checkBox.SetLabel("Правильно")
                checkBox.SetValue(True)
                self.count += 1
            else:
                checkBox.SetLabel("Неправильно")
                checkBox.SetValue(False)

            self.grid.Add(labelCorrect, 0, wx.EXPAND)
            self.grid.Add(playOrigBtn, 0, wx.EXPAND)
            self.grid.Add(labelRecord, 0, wx.EXPAND)
            self.grid.Add(playRecBtn, 0, wx.EXPAND)
            self.grid.Add(checkBox, 0, wx.EXPAND)

            self.all_check_box.append(checkBox)

        self.countLabel = wx.StaticText(self, label="Правильно пройденных тестов {}".format(self.count))

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Продолжить", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.grid)
        self.mainSizer.Add(self.countLabel)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()


    def updateCheckBox(self, event):
        check_box = event.GetEventObject()
        if check_box.IsChecked():
            check_box.SetLabel("Правильно")
            self.count += 1
        else:
            check_box.SetLabel("Неправильно")
            self.count -= 1
        self.updateCountLabel()

    def updateCountLabel(self):
        self.countLabel.SetLabel("Правильно пройденных тестов {}".format(self.count))

    def layoutControls(self):
        wx.InitAllImageHandlers()

    def playRecord(self, event):
        btn = event.GetEventObject()
        play_file(self.btn_to_file[btn.GetId()])
        
    def nextPanel(self, event):
        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()
