import random
import wx
import wx.media
from wx.lib.intctrl import IntCtrl

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

        soundToolChoiceLabel = wx.StaticText(self, -1, "Источник звука", size=(125, 25))
        soundTools = ['Свободное звуковое поле', 'Наушники']
        self.soundToolChoice = wx.Choice (self, choices=soundTools)
        self.soundToolChoice.Bind(wx.EVT_CHOICE, self.setSoundTool)
        self.soundToolChoice.SetSelection(0)

        voiceChoiceLabel = wx.StaticText(self, -1, "Голос озвучки", size=(125, 25))
        voice = ['Мужчина', 'Женщина']
        self.voiceChoice = wx.Choice (self, choices=voice)
        self.voiceChoice.Bind(wx.EVT_CHOICE, self.setVoice)
        self.voiceChoice.SetSelection(0)

        earSettingsLabel = wx.StaticText(self, -1, "Настройки для:", size=(125, 25))
        leftEarLabel = wx.StaticText(self, -1, "Левое ухо", size=(125, 25))
        rightEarLabel = wx.StaticText(self, -1, "Правое ухо", size=(125, 25))

        hearingToolLabel = wx.StaticText(self, -1, "Вид аппарата", size=(125, 25))
        hearingTools = ['Слуховой аппарат', 'Кохлеарный имплантат']
        self.leftToolChoice = wx.Choice(self, choices=hearingTools)
        self.leftToolChoice.Bind(wx.EVT_CHOICE, self.setLeftTool)
        self.leftToolChoice.SetSelection(0)
        self.rightToolChoice = wx.Choice(self, choices=hearingTools)
        self.rightToolChoice.Bind(wx.EVT_CHOICE, self.setRightTool)
        self.rightToolChoice.SetSelection(0)

        hearingMethodLabel = wx.StaticText(self, -1, "Метод коррекции слуха", size=(125, 30))
        methods = ['АД', 'АС', 'Бинаурально']
        self.leftMethodChoice = wx.Choice(self, choices=methods)
        self.leftMethodChoice.Bind(wx.EVT_CHOICE, self.setLeftMethod)
        self.leftMethodChoice.SetSelection(0)
        self.rightMethodChoice = wx.Choice(self, choices=methods)
        self.rightMethodChoice.Bind(wx.EVT_CHOICE, self.setRightMethod)
        self.rightMethodChoice.SetSelection(0)

        hearingAidLabel = wx.StaticText(self, -1, "Вид слухового аппарата", size=(125, 25))
        self.hearingAidText = wx.TextCtrl(self, size=(150, 25))

        self.available_words_wav = return_file_names_with_extension(self.recognition_service_settings.words_dir, extension=".wav")

        available_noises_wav = [WITHOUT_NOISE_OPTION]
        available_noises_wav.extend(return_file_names_with_extension(self.recognition_service_settings.noises_dir, extension=".wav"))

        self.fioLabel = wx.StaticText(self, label="{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel = wx.StaticText(self, label="{} {}".format("Год рождения: ", self.testing_model.birthday))

        self.filesBox = wx.CheckListBox(self, choices=self.available_words_wav)
        self.filesBox.Bind(wx.EVT_CHECKLISTBOX, self.addOrRemoveTestingItems)

        self.noiseLabel = wx.StaticText(self, label="Шумы: ")

        self.noisesBox = wx.Choice(self, choices=available_noises_wav, size=(150,30))
        self.noisesBox.SetSelection(0)
        self.noisesBox.Bind(wx.EVT_CHOICE, self.setNoise)

        self.filesNumber = wx.StaticText(self, label="{} {}".format(self.filesNumberLabel, self.test_setting.audioFilesNumber))

        self.nextBtn = wx.Button(self, style=wx.SL_INVERSE, label="Начать воспроизведение", size=(150, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.randomRecordLabel = wx.StaticText(self, label="Кол-во случайных записей")
        self.randomRecordCnt = wx.lib.intctrl.IntCtrl(self, size=(150, 25), min=0, max=len(self.available_words_wav),
                                                      value=len(self.available_words_wav) // 2, limited=True)
        self.chooseRandomBtn = wx.Button(self, style=wx.SL_INVERSE, label="Выбрать записи", size=(150,30))
        self.chooseRandomBtn.Bind(wx.EVT_BUTTON, self.chooseRandom)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.soundToolChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.voiceChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.earSettingsLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hearingToolChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hearingMethodChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hearingAidSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vNoiseSizer = wx.BoxSizer(wx.VERTICAL)
        self.vRandomSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer.Add(self.fioLabel)
        self.mainSizer.Add(self.birthdayLabel)

        self.soundToolChoiceSizer.Add(soundToolChoiceLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.soundToolChoiceSizer.Add(self.soundToolChoice)

        self.voiceChoiceSizer.Add(voiceChoiceLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.voiceChoiceSizer.Add(self.voiceChoice)

        self.earSettingsLabelSizer.Add(earSettingsLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.earSettingsLabelSizer.Add(leftEarLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.earSettingsLabelSizer.Add(rightEarLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        self.hearingToolChoiceSizer.Add(hearingToolLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingToolChoiceSizer.Add(self.leftToolChoice)
        self.hearingToolChoiceSizer.Add(self.rightToolChoice)

        self.hearingMethodChoiceSizer.Add(hearingMethodLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingMethodChoiceSizer.Add(self.leftMethodChoice)
        self.hearingMethodChoiceSizer.Add(self.rightMethodChoice)

        self.hearingAidSizer.Add(hearingAidLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingAidSizer.Add(self.hearingAidText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        self.vNoiseSizer.Add(self.noiseLabel)
        self.vNoiseSizer.Add(self.noisesBox)
        
        self.vRandomSizer.Add(self.randomRecordLabel)
        self.vRandomSizer.Add(self.randomRecordCnt)
        self.vRandomSizer.Add(self.chooseRandomBtn)

        self.hSizer.Add(self.filesBox)
        self.hSizer.Add(self.vNoiseSizer)
        self.hSizer.Add(self.vRandomSizer)

        self.mainSizer.Add(self.soundToolChoiceSizer)
        self.mainSizer.Add(self.voiceChoiceSizer)
        self.mainSizer.Add(self.earSettingsLabelSizer)
        self.mainSizer.Add(self.hearingToolChoiceSizer)
        self.mainSizer.Add(self.hearingMethodChoiceSizer)
        self.mainSizer.Add(self.hearingAidSizer)
        self.mainSizer.Add(self.hSizer)
        self.mainSizer.Add(self.filesNumber)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def update(self):
        self.fioLabel.SetLabel("{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel.SetLabel("{} {}".format("Год рождения: ", self.testing_model.birthday))

    def nextPanel(self, event):
        if len(self.testing_model.testingItems) == 0:
            dial = wx.MessageDialog(self.parent, message="Нужно выбрать хотя бы одну запись", caption="Ошибка",
                             style=wx.OK|wx.CENTER, pos=wx.DefaultPosition)
            dial.ShowModal()
            return
        self.test_setting.hearingAidType = self.hearingAidText.GetValue()

        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def resetFilesBox(self):
        for item in self.filesBox.GetCheckedItems():
            self.filesBox.Check(item, check=False)

    def chooseRandom(self, event):
        self.resetFilesBox()
        choosenItems = random.sample(range(len(self.available_words_wav)), self.randomRecordCnt.GetValue())
        for item in choosenItems:
            self.filesBox.Check(item, check=True)
        
        self.addOrRemoveTestingItems(None)

    def addOrRemoveTestingItems(self, event):
        self.testing_model.testingItems = []

        for item in self.filesBox.GetCheckedStrings():
            test_item = TestingItem()
            test_item.initialAudioFilePath = item
            test_item.initialText = item.split('.')[0].lower()
            self.testing_model.testingItems.append(test_item)

        self.test_setting.audioFilesNumber = len(self.testing_model.testingItems)
        self.filesNumber.SetLabel("{} {}".format(self.filesNumberLabel, self.test_setting.audioFilesNumber))

    def setNoise(self, event):
        selected_item = self.noisesBox.GetString(self.noisesBox.GetSelection())
        if selected_item == WITHOUT_NOISE_OPTION:
            self.test_setting.noiseFile = ''
        else:
            self.test_setting.noiseFile = selected_item

    def setSoundTool(self, event):
        self.test_setting.soundTool = self.soundToolChoice.GetSelection()

    def setVoice(self, event):
        self.test_setting.voice = self.voiceChoice.GetSelection()

    def setLeftTool(self, event):
        self.test_setting.leftTool = self.leftToolChoice.GetSelection()

    def setRightTool(self, event):
        self.test_setting.rightTool = self.rightToolChoice.GetSelection()

    def setLeftMethod(self, event):
        self.test_setting.leftMethod = self.leftMethodChoice.GetSelection()

    def setRightMethod(self, event):
        self.test_setting.rightMethod = self.rightMethodChoice.GetSelection()