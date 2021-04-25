import os
import wx
import wx.media
from datetime import datetime

import patient_testing_model
from patient_testing_model import *
from recognition_service import *
from microphone_service import *
from wx.lib.pubsub import pub

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PatientInfoPanel(wx.Panel):

    def __init__(self, parent, next_panel):
        wx.Panel.__init__(self, parent=parent)

        self.frame = parent
        self.SetSize((800, 600))
        self.layoutControls()
        self.next_panel = next_panel
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        self.patient = patient_testing_model.PatientTestingModel()


    def layoutControls(self):
        wx.InitAllImageHandlers()

        panel = self
        verticalBoxSizer = wx.BoxSizer(wx.VERTICAL)

        helpBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpLabel = wx.StaticText(self, label="Заполните информацию о пациенте")
        helpBoxSizer.Add(self.helpLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(helpBoxSizer)

        fioBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        fioLabel = wx.StaticText(panel, -1, "ФИО", size=(125,25))
        fioBoxSizer.Add(fioLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        self.fioText = wx.TextCtrl(panel)
        fioBoxSizer.Add(self.fioText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.fioText.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        verticalBoxSizer.Add(fioBoxSizer)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        birthdayLabel = wx.StaticText(panel, -1, "Год гождения")

        hbox2.Add(birthdayLabel, 1, wx.ALIGN_LEFT|wx.ALL,5)
        self.birthdayText = wx.TextCtrl(panel, size=(125,25), style = wx.TE_PASSWORD)
        self.birthdayText.SetMaxLength(4)

        hbox2.Add(self.birthdayText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(hbox2)
        self.birthdayText.Bind(wx.EVT_TEXT_MAXLEN, self.OnMaxLen)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        l4 = wx.StaticText(panel, -1, "Дата тестирования")

        hbox4.Add(l4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t4 = wx.TextCtrl(panel, size=(125,25), value=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), style = wx.TE_READONLY|wx.TE_CENTER)

        hbox4.Add(self.t4,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(hbox4)

        nextButtonBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Продолжить", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)
        nextButtonBoxSizer.Add(self.nextBtn, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(nextButtonBoxSizer)

        panel.SetSizer(verticalBoxSizer)

        self.Layout()


    def OnKeyTyped(self, event):
        print(event.GetString())


    def OnEnterPressed(self,event):
        print("Enter pressed")


    def OnMaxLen(self,event):
        print("Maximum length reached")

    def nextPanel(self, event):
        if self.next_panel == None:
            return
        fio = self.fioText.GetValue().split()
        if len(fio) > 3:
            print("Too many words, truncating to first 3")
        if str.isalpha(fio[0]) is False:
            print("Please enter valid second name")
            return
        if str.isalpha(fio[1]) is False:
            print("Please enter valid first name")
            return
        self.patient.secondName = fio[0]
        self.patient.firstName = fio[1]
        if len(fio) == 3:
            if str.isalpha(fio[2]) is False:
                print("Please enter valid middle name")
                return
            self.patient.middleName = fio[2]
        if str.isnumeric(self.birthdayText.GetValue()) is False:
            print("Please enter valid birth year")
            return
        self.patient.birthday = int(self.birthdayText.GetValue(), base=10)
        if self.patient.birthday < 1900:
            print("Please enter valid birth year")
            return
        self.patient.testDay = self.t4.GetValue()
        print(self.patient.birthday)
        print(self.patient.secondName)
        print(self.patient.firstName)
        print(self.patient.middleName)
        pub.sendMessage("panelListener", message=self.patient)
        self.Hide()
        self.next_panel.Show()
        self.Layout()