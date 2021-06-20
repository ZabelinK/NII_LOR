import random
import wx
import wx.media
from wx.lib.intctrl import IntCtrl
from wx.lib.agw.customtreectrl import CustomTreeCtrl, EVT_TREE_ITEM_CHECKED

import os

from models.patient_testing_model import *
from utils.utils import *
from utils.constants import WITHOUT_NOISE_OPTION

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class AudioChoosingPanel(wx.Panel):

    filesNumberLabel = "Количество файлов: "

    def __init__(self, parent, testing_model, test_setting, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent

        self.testing_model = testing_model
        self.test_setting = test_setting
        self.recognition_service_settings = recognition_service_settings

        self.SetSize((800, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        available_noises_wav = [WITHOUT_NOISE_OPTION]
        available_noises_wav.extend(return_file_names_with_extension(self.recognition_service_settings.noises_dir, extension=".wav"))

        self.noiseLabel = wx.StaticText(self, label="Шумы: ")

        self.noisesBox = wx.Choice(self, choices=available_noises_wav, size=(150,30))
        self.noisesBox.SetSelection(0)
        self.noisesBox.Bind(wx.EVT_CHOICE, self.setNoise)

        self.filesNumber = wx.StaticText(self, label="{} {}".format(self.filesNumberLabel, self.test_setting.audioFilesNumber))

        self.choosingAudioTree = CustomTreeCtrl(self, style=wx.SL_INVERSE, size=(300, 200))
        self.constructAudioTree()
        self.choosingAudioTree.ExpandAll()
        self.choosingAudioTree.Bind(EVT_TREE_ITEM_CHECKED, self.addOrRemoveTestingItems)

        self.nextBtn = wx.Button(self, style=wx.SL_INVERSE, label="Начать воспроизведение", size=(150, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.randomRecordLabel = wx.StaticText(self, label="Кол-во случайных записей")
        self.randomRecordCnt = wx.lib.intctrl.IntCtrl(self, size=(150, 25), min=0, max=len(self.check_box_items),
                                                      value=len(self.check_box_items) // 2, limited=True)
        self.chooseRandomBtn = wx.Button(self, style=wx.SL_INVERSE, label="Выбрать записи", size=(150,30))
        self.chooseRandomBtn.Bind(wx.EVT_BUTTON, self.chooseRandom)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vNoiseSizer = wx.BoxSizer(wx.VERTICAL)
        self.vRandomSizer = wx.BoxSizer(wx.VERTICAL)

        self.vNoiseSizer.Add(self.noiseLabel)
        self.vNoiseSizer.Add(self.noisesBox)
        
        self.vRandomSizer.Add(self.randomRecordLabel)
        self.vRandomSizer.Add(self.randomRecordCnt)
        self.vRandomSizer.Add(self.chooseRandomBtn)

#        self.hSizer.Add(self.filesBox)
        self.hSizer.Add(self.choosingAudioTree)
        self.hSizer.Add(self.vNoiseSizer)
        self.hSizer.Add(self.vRandomSizer)


        self.mainSizer.Add(self.hSizer)
        self.mainSizer.Add(self.filesNumber)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def update(self):
        pass

    def nextPanel(self, event):
        if len(self.testing_model.testingItems) == 0:
            dial = wx.MessageDialog(self.parent, message="Нужно выбрать хотя бы одну запись", caption="Ошибка",
                             style=wx.OK|wx.CENTER, pos=wx.DefaultPosition)
            dial.ShowModal()
            return

        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def constructAudioTree(self):
        words_path = self.recognition_service_settings.words_dir
        self.generic_tree_items = {
                               words_path : self.choosingAudioTree.AddRoot("words")
                             }
        self.check_box_items = []

        for root, dirs, files in os.walk(words_path):
            root_tree_item = self.generic_tree_items[root]
            for dir in dirs:
                self.generic_tree_items[root + dir] = self.choosingAudioTree.AppendItem(root_tree_item, dir)

            for file in files:
                check_box_item = self.choosingAudioTree.AppendItem(root_tree_item, file, ct_type=1)
                self.generic_tree_items[root + os.sep + file] = check_box_item
                self.check_box_items.append(check_box_item)

    def resetFilesBox(self):
        for check_box_item in self.check_box_items:
            check_box_item.Check(checked=False)

    def chooseRandom(self, event):
        self.resetFilesBox()
        choosen_items = random.sample(range(len(self.check_box_items)), self.randomRecordCnt.GetValue())
        for choosen_item_idx in choosen_items:
            self.check_box_items[choosen_item_idx].Check(checked=True)
        
        self.choosingAudioTree.Refresh()

        self.addOrRemoveTestingItems(None)

    def addOrRemoveTestingItems(self, event):
        self.testing_model.testingItems = []

        for path, tree_item in self.generic_tree_items.items():
            if not tree_item.IsChecked():
                continue

            test_item = TestingItem()
            test_item.initialAudioFilePath = path.replace(self.recognition_service_settings.words_dir, '')
            test_item.initialText = path.split(os.sep)[-1].split('.')[0].lower()
            self.testing_model.testingItems.append(test_item)

        self.test_setting.audioFilesNumber = len(self.testing_model.testingItems)
        self.filesNumber.SetLabel("{} {}".format(self.filesNumberLabel, self.test_setting.audioFilesNumber))

    def setNoise(self, event):
        selected_item = self.noisesBox.GetString(self.noisesBox.GetSelection())
        if selected_item == WITHOUT_NOISE_OPTION:
            self.test_setting.noiseFile = ''
        else:
            self.test_setting.noiseFile = selected_item