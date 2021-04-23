import os
import wx
import wx.media
from datetime import datetime

from patient_testing_model import *
from recognition_service import *
from microphone_service import *

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


    def layoutControls(self):
        wx.InitAllImageHandlers()

        panel = self
        verticalBoxSizer = wx.BoxSizer(wx.VERTICAL)

        helpBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpLabel = wx.StaticText(self, label="Заполните информацию о пациенте")
        helpBoxSizer.Add(self.helpLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(helpBoxSizer)

        fioBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        fioLabel = wx.StaticText(panel, -1, "ФИО")
        fioBoxSizer.Add(fioLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        self.fioText = wx.TextCtrl(panel)
        fioBoxSizer.Add(self.fioText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.fioText.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        verticalBoxSizer.Add(fioBoxSizer)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        birthdayLabel = wx.StaticText(panel, -1, "Год гождения")

        hbox2.Add(birthdayLabel, 1, wx.ALIGN_LEFT|wx.ALL,5)
        self.birthdayText = wx.TextCtrl(panel, style = wx.TE_PASSWORD)
        self.birthdayText.SetMaxLength(5)

        hbox2.Add(self.birthdayText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(hbox2)
        self.birthdayText.Bind(wx.EVT_TEXT_MAXLEN, self.OnMaxLen)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        l4 = wx.StaticText(panel, -1, "Дата тестирования")

        hbox4.Add(l4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t4 = wx.TextCtrl(panel, value=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), style = wx.TE_READONLY|wx.TE_CENTER)

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

        self.Hide()
        self.next_panel.Show()
        self.Layout()