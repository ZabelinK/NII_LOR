import os
import wx
import wx.media
from datetime import datetime

import patient_testing_model
from patient_testing_model import *
from recognition_service import *
from microphone_service import *
from constants import DEFAULT_USER_FIO
from constants import DEFAULT_BIRTHDAY
from constants import DEFAULT_DOCTOR_FIO

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PatientInfoPanel(wx.Panel):

    def __init__(self, parent, testing_model):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.patient = testing_model

        self.SetSize((800, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def update(self):
        pass

    def layoutControls(self):
        wx.InitAllImageHandlers()

        panel = self
        verticalBoxSizer = wx.BoxSizer(wx.VERTICAL)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        l4 = wx.StaticText(panel, -1, "Дата тестирования")

        hbox4.Add(l4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t4 = wx.TextCtrl(panel, size=(125,25), value=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), style = wx.TE_READONLY|wx.TE_CENTER)

        hbox4.Add(self.t4,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(hbox4)

        helpBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpLabel = wx.StaticText(self, label="Заполните информацию о пациенте")
        helpBoxSizer.Add(self.helpLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(helpBoxSizer)

        fioBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        fioLabel = wx.StaticText(panel, -1, "ФИО пациента", size=(125,25))
        fioBoxSizer.Add(fioLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        self.fioText = wx.TextCtrl(panel)
        fioBoxSizer.Add(self.fioText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.fioText.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        verticalBoxSizer.Add(fioBoxSizer)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        birthdayLabel = wx.StaticText(panel, -1, "Год гождения")

        hbox2.Add(birthdayLabel, 1, wx.ALIGN_LEFT|wx.ALL,5)
        self.birthdayText = wx.TextCtrl(panel, size=(125,25))
        self.birthdayText.SetMaxLength(4)

        hbox2.Add(self.birthdayText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(hbox2)
        self.birthdayText.Bind(wx.EVT_TEXT_MAXLEN, self.OnMaxLen)

        helpDoctorBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpDoctorLabel = wx.StaticText(self, label="Заполните информацию о враче")
        helpDoctorBoxSizer.Add(self.helpDoctorLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(helpDoctorBoxSizer)

        doctorFioBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        doctorFioLabel = wx.StaticText(panel, -1, "ФИО врача", size=(125, 25))
        doctorFioBoxSizer.Add(doctorFioLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        self.doctorFioText = wx.TextCtrl(panel)
        doctorFioBoxSizer.Add(self.doctorFioText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.doctorFioText.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        verticalBoxSizer.Add(doctorFioBoxSizer)

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
        fio = self.fioText.GetValue()

        if not fio:
            fio = DEFAULT_USER_FIO

        fio_parts = fio.split()
        if len(fio_parts) > 3:
            print("Too many words, truncating to first 3")
        if str.isalpha(fio_parts[0]) is False:
            print("Please enter valid second name")
            return
        if str.isalpha(fio_parts[1]) is False:
            print("Please enter valid first name")
            return
        self.patient.secondName = fio_parts[0]
        self.patient.firstName = fio_parts[1]
        if len(fio_parts) == 3:
            if str.isalpha(fio_parts[2]) is False:
                print("Please enter valid middle name")
                return
            self.patient.middleName = fio_parts[2]

        birthdayText = self.birthdayText.GetValue()
        if not birthdayText:
            birthdayText = DEFAULT_BIRTHDAY

        if str.isnumeric(birthdayText) is False:
            print("Please enter valid birth year")
            return

        self.patient.birthday = int(birthdayText, base=10)
        if self.patient.birthday < 1900:
            print("Please enter valid birth year")
            return

        self.patient.testDay = self.t4.GetValue()

        doctorFio = self.doctorFioText.GetValue()

        if not doctorFio:
            doctorFio = DEFAULT_DOCTOR_FIO

        doctorFio_parts = doctorFio.split()
        if len(doctorFio_parts) > 3:
            print("Too many words, truncating to first 3")
        if str.isalpha(doctorFio_parts[0]) is False:
            print("Please enter valid second name")
            return
        if str.isalpha(doctorFio_parts[1]) is False:
            print("Please enter valid first name")
            return
        self.patient.doctorSecondName = doctorFio_parts[0]
        self.patient.doctorFirstName = doctorFio_parts[1]
        if len(doctorFio_parts) == 3:
            if str.isalpha(doctorFio_parts[2]) is False:
                print("Please enter valid middle name")
                return
            self.patient.doctorMiddleName = doctorFio_parts[2]

        print(self.patient.birthday)
        print(self.patient.secondName)
        print(self.patient.firstName)
        print(self.patient.middleName)
        print(self.patient.doctorSecondName)
        print(self.patient.doctorFirstName)
        print(self.patient.doctorMiddleName)

        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()