import random
import wx
import wx.media
from wx.lib.intctrl import IntCtrl
from wx.lib.agw.customtreectrl import CustomTreeCtrl, EVT_TREE_ITEM_CHECKED

import os

from models.patient_testing_model import *
from utils.utils import *
from utils.constants import WITHOUT_NOISE_OPTION
from utils.error_handling import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class AudioChoosingPanel(wx.Panel):

    ExpandableType = 0
    CheckableType = 1
    filesNumberLabel = "Количество файлов: "

    def __init__(self, parent, testing_model, test_setting, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent

        self.testing_model = testing_model
        self.test_setting = test_setting
        self.recognition_service_settings = recognition_service_settings

        self.SetSize((700, 700))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):

        wx.InitAllImageHandlers()

        available_noises_wav = [WITHOUT_NOISE_OPTION]
        available_noises_wav.extend(return_file_names_with_extension(self.recognition_service_settings.noises_dir, extension=".wav"))

        # Title initialization
        self.title = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_title = wx.StaticText(self, -1, "Шаг 3. Выбор записей для тестирования")
        self.title.Add(self.panel_title, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        # Voice choice initialization
        voiceChoiceLabel = wx.StaticText(self, -1, "Голос озвучки", size=(125, 25))
        voice = ['Мужчина', 'Женщина']
        self.voiceChoice = wx.Choice(self, choices=voice)
        self.voiceChoice.Bind(wx.EVT_CHOICE, self.setVoice)
        self.voiceChoice.SetSelection(0)

        # Play mode initialization
        self.playModeLabel = wx.StaticText(self, label="Режим воспроизведения:")
        modes = ['Автоматический            ', 'Поэтапный']
        self.playModeRadioBox = wx.RadioBox(self, choices=modes)
        self.playModeRadioBox.Bind(wx.EVT_RADIOBOX, self.setPlayMode)
        self.playModeRadioBox.SetSelection(0)

        self.delayLabel = wx.StaticText(self, label="Задержка (сек):   ")
        self.delaySlider = wx.Slider(self, value=self.test_setting.delay, minValue=1, maxValue=10, size=(200, 30),
                                     style=wx.SL_HORIZONTAL | wx.SL_VALUE_LABEL | wx.SL_MIN_MAX_LABELS | wx.SL_AUTOTICKS)
        self.delaySlider.Bind(wx.EVT_SCROLL, self.setDelay)

        # Noise choice initialization
        self.noiseLabel = wx.StaticText(self, label="Шумы: ")

        self.noisesBox = wx.Choice(self, choices=available_noises_wav, size=(300, 50))
        self.noisesBox.SetSelection(0)
        self.noisesBox.Bind(wx.EVT_CHOICE, self.setNoise)

        # AudioTree and random record numbers initialization
        self.choosingAudioTree = CustomTreeCtrl(self, style=wx.SL_INVERSE, size=(300, 500))
        self.constructAudioTree()
        extendables = self.returnAllNonEmptyExtendableItems()
        self.fields_to_item = {}
        self.vRandomMenu = wx.BoxSizer(wx.VERTICAL)
        print(extendables)
        for extendable in extendables:
            label = wx.StaticText(self, label="{}".format(extendable.GetText()))
            randomCnt =  wx.lib.intctrl.IntCtrl(self, size=(150, 25), min=0, max=self.getCheckableNumber(extendable),
                                                      value=self.getCheckableNumber(extendable) // 2, limited=True)
            self.vRandomMenu.Add(label)
            self.vRandomMenu.Add(randomCnt)
            self.fields_to_item[randomCnt] = extendable
        
        self.randomByPartBtn = wx.Button(self, style=wx.SL_INVERSE, label="Выбрать случайно для\n каждой категории", size=(150, 50))
        self.randomByPartBtn.Bind(wx.EVT_BUTTON, self.randomByPart)
        self.vRandomMenu.Add(self.randomByPartBtn)

        self.choosingAudioTree.ExpandAll()
        self.choosingAudioTree.Bind(EVT_TREE_ITEM_CHECKED, self.addOrRemoveTestingItems)

        self.randomRecordLabel = wx.StaticText(self, label="             Количество \n      случайных записей")
        self.randomRecordCnt = wx.lib.intctrl.IntCtrl(self, size=(150, 25), min=0, max=len(self.check_box_items),
                                                      value=len(self.check_box_items) // 2, limited=True)
        self.chooseRandomBtn = wx.Button(self, style=wx.SL_INVERSE,
                                         label="Выбрать случайно\nбез учёта категории", size=(150, 50))
        self.chooseRandomBtn.Bind(wx.EVT_BUTTON, self.chooseRandom)

        # Files number and next-button initialization
        self.filesNumber = wx.StaticText(self, label="{} {}".format(self.filesNumberLabel,
                                                                    self.test_setting.audioFilesNumber))

        self.nextBtn = wx.Button(self, style=wx.SL_INVERSE, label="Начать воспроизведение", size=(150, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.prevBtn = wx.Button(self, style=wx.SL_INVERSE, label="Назад", size=(150, 30))
        self.prevBtn.Bind(wx.EVT_BUTTON, self.prevPanel)
        #TODO: когда несколько раз щелкаешь вперед-назад окно сворачивается

        # Sizers initialization
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vRandomSizer = wx.BoxSizer(wx.VERTICAL)
        self.hDelaySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vSettingsSizer = wx.BoxSizer(wx.VERTICAL)
        self.hRandomSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prevNextSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.voiceChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)

        
        self.vRandomSizer.Add(self.randomRecordLabel)
        self.vRandomSizer.Add(self.randomRecordCnt)
        self.vRandomSizer.Add(self.chooseRandomBtn)


        self.hRandomSizer.Add(self.vRandomSizer)
        self.hRandomSizer.Add(self.vRandomMenu)

        self.hDelaySizer.Add(self.delayLabel)
        self.hDelaySizer.Add(self.delaySlider)

        self.vSettingsSizer.Add(self.playModeLabel)
        self.vSettingsSizer.Add(self.playModeRadioBox)
        self.vSettingsSizer.Add(self.hDelaySizer)
        self.vSettingsSizer.Add(self.hDelaySizer)
        self.vSettingsSizer.Add(self.noiseLabel)
        self.vSettingsSizer.Add(self.noisesBox)
        self.vSettingsSizer.Add(self.hRandomSizer)

#        self.hSizer.Add(self.filesBox)
        self.hSizer.Add(self.choosingAudioTree)
        self.hSizer.Add(self.vSettingsSizer)

        self.prevNextSizer.Add(self.prevBtn)
        self.prevNextSizer.Add(self.nextBtn)

        self.voiceChoiceSizer.Add(voiceChoiceLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.voiceChoiceSizer.Add(self.voiceChoice)

        self.mainSizer.Add(self.title)
        self.mainSizer.Add(self.voiceChoiceSizer)
        self.mainSizer.Add(self.hSizer)
        self.mainSizer.Add(self.filesNumber)
        self.mainSizer.Add(self.prevNextSizer)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def update(self):
        self.prev_size = self.parent.GetSize()
        self.parent.SetSize(self.GetSize())

    def nextPanel(self, event):
        if len(self.testing_model.testingItems) == 0:
            dial = wx.MessageDialog(self.parent, message="Нужно выбрать хотя бы одну запись", caption="Ошибка",
                             style=wx.OK|wx.CENTER, pos=wx.DefaultPosition)
            dial.ShowModal()
            return

        self.parent.SetSize(self.prev_size)
        self.Hide()
        next_panel = next(self.parent.current_panel)
        if self.playModeRadioBox.GetSelection() == 0:   # auto
            next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def prevPanel(self, event):
        self.parent.SetSize(self.prev_size)
        self.Hide()
        prev_panel = next(return_to_prev_page(self.parent.current_panel, self.parent.number_of_frames))
        prev_panel.update()
        prev_panel.Show()
        self.Layout()

    def returnAllNonEmptyExtendableItemsImpl(self, item):
        childrens = item.GetChildren()
        extendable = []
        for children in childrens:
            if children.GetType() == self.ExpandableType:
                extendable.extend(self.returnAllNonEmptyExtendableItemsImpl(children))
        
        if self.getCheckableNumber(item):
            extendable.append(item)
        
        return extendable
        
    def returnAllNonEmptyExtendableItems(self):
        root = self.choosingAudioTree.GetRootItem()
        return self.returnAllNonEmptyExtendableItemsImpl(root)

    def getCheckableNumber(self, item):
        return sum(1 for children in item.GetChildren() if children.GetType() == self.CheckableType)

    def getCheckable(self, item):
        return list(filter(lambda item: item.GetType() == self.CheckableType, item.GetChildren()))

    def constructAudioTree(self):
        if self.test_setting.voice == 0:
            self.recognition_service_settings.words_dir = '..\\data_set\\\\records\\man\\'
        if self.test_setting.voice == 1:
            self.recognition_service_settings.words_dir = '..\\data_set\\\\records\\woman\\'
        words_path = self.recognition_service_settings.words_dir
        self.generic_tree_items = {
                               words_path : self.choosingAudioTree.AddRoot("words")
                             }
        self.check_box_items = []

        try:
            for root, dirs, files in os.walk(words_path):
                root_tree_item = self.generic_tree_items[root]
                for dir in dirs:
                    self.generic_tree_items[root + dir] = self.choosingAudioTree.AppendItem(root_tree_item, dir)

                for file in files:
                    check_box_item = self.choosingAudioTree.AppendItem(root_tree_item, file, ct_type=1)
                    self.generic_tree_items[root + os.sep + file] = check_box_item
                    self.check_box_items.append(check_box_item)
        except KeyError as error:
            exception_logger(error)
            error_message(self, error)

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

    def randomByPart(self, event):
        self.resetFilesBox()

        for field, extendable in self.fields_to_item.items():
            checkable = self.getCheckable(extendable)
            choosen_items = random.sample(range(len(checkable)), field.GetValue())

            for choosen_item_idx in choosen_items:
                checkable[choosen_item_idx].Check(checked=True)

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

    def setPlayMode(self, event):
        choise = self.playModeRadioBox.GetSelection()
        if choise == 1:                 # staged
            self.delayLabel.Hide()
            self.delaySlider.Hide()
        else:                           # auto
            self.delayLabel.Show()
            self.delaySlider.Show()

    def setDelay(self, event):
        self.test_setting.delay = self.delaySlider.GetValue()

    def setVoice(self, event):
        self.test_setting.voice = self.voiceChoice.GetSelection()
        self.choosingAudioTree.DeleteAllItems()
        self.constructAudioTree()
        self.choosingAudioTree.ExpandAll()