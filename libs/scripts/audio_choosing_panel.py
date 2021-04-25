import os
import wx
import wx.media

import patient_testing_model
from patient_testing_model import *
from recognition_service import *
from microphone_service import *
from utils import *

from constants import PATH_TO_WORDS, PATH_TO_NOISES, WITHOUT_NOISE_OPTION

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class AudioChoosingPanel(wx.Panel):

    filesNumberLabel = "Количество файлов: "

    def __init__(self, parent, next_panel, testing_model):
        wx.Panel.__init__(self, parent=parent)

        self.frame = parent

        self.testing_model = testing_model

        self.SetSize((800, 600))
        self.layoutControls()
        self.next_panel = next_panel
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        available_words_wav = return_file_names_with_extension(PATH_TO_WORDS, extension=".wav")

        available_noises_wav = [WITHOUT_NOISE_OPTION]
        available_noises_wav.extend(return_file_names_with_extension(PATH_TO_NOISES, extension=".wav"))

        self.filesBox = wx.CheckListBox(self, choices=available_words_wav)
        self.filesBox.Bind(wx.EVT_CHECKLISTBOX, self.addOrRemoveTestingItems)

        self.noiseLabel = wx.StaticText(self, label="Шумы: ")

        self.noisesBox = wx.Choice(self, choices=available_noises_wav, size=(150,30))
        self.noisesBox.Bind(wx.EVT_CHOICE, self.setNoise)

        self.filesNumber = wx.StaticText(self, label="{} {}".format(self.filesNumberLabel, self.testing_model.testingSettings.audioFilesNumber))

        self.nextBtn = wx.Button(self, style=wx.SL_INVERSE, label="Начать воспроизведение", size=(150, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.hSizer.Add(self.filesBox)
        self.hSizer.Add(self.noiseLabel)
        self.hSizer.Add(self.noisesBox)

        self.mainSizer.Add(self.hSizer)
        self.mainSizer.Add(self.filesNumber)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def nextPanel(self, event):
        if self.next_panel == None:
            return

        print("Testing Model content {}".format(self.testing_model))

        self.Hide()
        self.next_panel.Show()
        self.Layout()

    def addOrRemoveTestingItems(self, event):
        self.testing_model.testingItems = []

        for item in self.filesBox.GetCheckedStrings():
            test_item = TestingItem()
            test_item.initialAudioFilePath = item
            test_item.initialText = item.split('.')[0]
            self.testing_model.testingItems.append(test_item)

        self.testing_model.testingSettings.audioFilesNumber = len(self.testing_model.testingItems)
        self.filesNumber.SetLabel("{} {}".format(self.filesNumberLabel, self.testing_model.testingSettings.audioFilesNumber))

    def setNoise(self, event):
        selected_item = self.noisesBox.GetString(self.noisesBox.GetSelection())
        if selected_item == WITHOUT_NOISE_OPTION:
            self.testing_model.testingSettings.noiseFile = ''
        else:
            self.testing_model.testingSettings.noiseFile = selected_item