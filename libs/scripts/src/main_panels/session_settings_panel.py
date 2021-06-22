import wx
import wx.media

from models.patient_testing_model import *
from utils.utils import *

class SessionSettingsPanel(wx.Panel):

    def __init__(self, parent, testing_model, test_setting):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent

        self.testing_model = testing_model
        self.test_setting = test_setting

        self.SetSize((800, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        soundToolChoiceLabel = wx.StaticText(self, -1, "Источник звука", size=(125, 25))
        soundTools = ['Свободное звуковое поле', 'Наушники']
        self.soundToolChoice = wx.Choice(self, choices=soundTools)
        self.soundToolChoice.Bind(wx.EVT_CHOICE, self.setSoundTool)
        self.soundToolChoice.SetSelection(0)
        self.test_setting.soundTool = 0

        voiceChoiceLabel = wx.StaticText(self, -1, "Голос озвучки", size=(125, 25))
        voice = ['Мужчина', 'Женщина']
        self.voiceChoice = wx.Choice(self, choices=voice)
        self.voiceChoice.Bind(wx.EVT_CHOICE, self.setVoice)
        self.voiceChoice.SetSelection(0)
        self.test_setting.voice = 0

        hearingMethodLabel = wx.StaticText(self, -1, "Метод коррекции слуха", size=(125, 30))
        methods = ['AS', 'AD', 'Бинаурально']
        self.methodChoice = wx.RadioBox(self, choices=methods)
        self.methodChoice.Bind(wx.EVT_RADIOBOX, self.setAnalysisMethod)
        self.methodChoice.SetSelection(0)
        self.test_setting.analysisMethod = 0

        earSettingsLabel = wx.StaticText(self, -1, "Настройки для:", size=(125, 25))
        hearingToolLabel = wx.StaticText(self, -1, "Вид аппарата", size=(125, 25))
        leftEarLabel = wx.StaticText(self, -1, "Левое ухо", size=(125, 25))
        rightEarLabel = wx.StaticText(self, -1, "Правое ухо", size=(125, 25))
        hearingTools = ['-', 'Слуховой аппарат', 'Кохлеарный имплантат']
        self.leftToolChoice = wx.Choice(self, choices=hearingTools)
        self.leftToolChoice.Bind(wx.EVT_CHOICE, self.setLeftTool)
        self.leftToolChoice.SetSelection(0)
        self.test_setting.leftTool = 0
        self.rightToolChoice = wx.Choice(self, choices=hearingTools)
        self.rightToolChoice.Bind(wx.EVT_CHOICE, self.setRightTool)
        self.rightToolChoice.SetSelection(0)
        self.test_setting.rightTool = 0

        hearingAidLabel = wx.StaticText(self, -1, "Информация об устройстве", size=(125, 25))
        self.hearingAidText = wx.TextCtrl(self, size=(250, 25))

        self.title = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_title = wx.StaticText(self, -1, "Шаг 2. Настройки тестирования аудиометрии")
        self.fioLabel = wx.StaticText(self, label="{} {}".format("ФИО: ",
                                                                 self.testing_model.firstName + " " + self.testing_model.middleName + " " + self.testing_model.secondName))
        self.birthdayLabel = wx.StaticText(self, label="{} {}".format("Год рождения: ", self.testing_model.birthday))

        self.nextBtn = wx.Button(self, style=wx.SL_INVERSE, label="Перейти к выбору записей", size=(170, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.soundToolChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.voiceChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.earSettingsLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hearingMethodChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hearingToolChoiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hearingAidSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.title.Add(self.panel_title, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.mainSizer.Add(self.title)
        self.mainSizer.Add(self.fioLabel)
        self.mainSizer.Add(self.birthdayLabel)

        self.soundToolChoiceSizer.Add(soundToolChoiceLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.soundToolChoiceSizer.Add(self.soundToolChoice)

        self.voiceChoiceSizer.Add(voiceChoiceLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.voiceChoiceSizer.Add(self.voiceChoice)

        self.earSettingsLabelSizer.Add(earSettingsLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingMethodChoiceSizer.Add(hearingMethodLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingMethodChoiceSizer.Add(self.methodChoice)
        self.earSettingsLabelSizer.Add(leftEarLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.earSettingsLabelSizer.Add(rightEarLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingToolChoiceSizer.Add(hearingToolLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingToolChoiceSizer.Add(self.leftToolChoice)
        self.hearingToolChoiceSizer.Add(self.rightToolChoice)

        self.hearingAidSizer.Add(hearingAidLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.hearingAidSizer.Add(self.hearingAidText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        self.mainSizer.Add(self.soundToolChoiceSizer)
        self.mainSizer.Add(self.voiceChoiceSizer)
        self.mainSizer.Add(self.hearingMethodChoiceSizer)
        self.mainSizer.Add(self.earSettingsLabelSizer)
        self.mainSizer.Add(self.hearingToolChoiceSizer)
        self.mainSizer.Add(self.hearingAidSizer)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def update(self):
        self.fioLabel.SetLabel("{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel.SetLabel("{} {}".format("Год рождения: ", self.testing_model.birthday))

    def nextPanel(self, event):
        self.test_setting.hearingAidType = self.hearingAidText.GetValue()

        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def setSoundTool(self, event):
        self.test_setting.soundTool = self.soundToolChoice.GetSelection()

    def setVoice(self, event):
        self.test_setting.voice = self.voiceChoice.GetSelection()

    def setLeftTool(self, event):
        self.test_setting.leftTool = self.leftToolChoice.GetSelection()

    def setRightTool(self, event):
        self.test_setting.rightTool = self.rightToolChoice.GetSelection()

    def setAnalysisMethod(self, event):
        choice = self.methodChoice.GetSelection()
        if choice == 0:
            self.leftToolChoice.Enable()
            self.rightToolChoice.SetSelection(0)
            self.rightToolChoice.Disable()
        elif choice == 1:
            self.leftToolChoice.SetSelection(0)
            self.leftToolChoice.Disable()
            self.rightToolChoice.Enable()
        else:
            self.leftToolChoice.Enable()
            self.rightToolChoice.Enable()
        self.test_setting.analysisMethod = choice
        self.test_setting.leftTool = self.leftToolChoice.GetSelection()
        self.test_setting.rightTool = self.rightToolChoice.GetSelection()




