import os
import wx.media
import wx.adv
from datetime import datetime

from extra_panels.error_panel import *
from utils.constants import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, '../../bitmaps')


class PatientInfoPanel(wx.Panel):

    def __init__(self, parent, testing_model):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.patient = testing_model

        self.SetSize((1000, 800))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def update(self):
        pass

    def layoutControls(self):
        wx.InitAllImageHandlers()

        panel = self
        verticalBoxSizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        panel_title = wx.StaticText(panel, -1, "Шаг 1. Информация о пациенте")
        l4 = wx.StaticText(panel, -1, "Дата тестирования", size=(190,25))

        title.Add(panel_title, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox4.Add(l4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t4 = wx.TextCtrl(panel, size=(150,25), value=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), style = wx.TE_READONLY|wx.TE_CENTER)

        hbox4.Add(self.t4,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(title)
        verticalBoxSizer.Add(hbox4)

        helpBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpLabel = wx.StaticText(self, label="Заполните информацию о пациенте")
        helpBoxSizer.Add(self.helpLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(helpBoxSizer)

        fioBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        fioLabel = wx.StaticText(panel, -1, "ФИО пациента", size=(170,25))
        fioBoxSizer.Add(fioLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT,5)

        self.fioText = wx.TextCtrl(panel, size=(220,25))
        fioBoxSizer.Add(self.fioText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.TOP, 5)
        self.fioText.Bind(wx.EVT_TEXT, self.OnKeyTyped)
        fioExLabel = wx.StaticText(panel, -1, "пр. Иванов Иван Иванович", size=(150, 25))
        fioBoxSizer.Add(fioExLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        verticalBoxSizer.Add(fioBoxSizer)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        birthdayLabel = wx.StaticText(panel, -1, "Дата рождения", size=(200, 25))

        hbox2.Add(birthdayLabel, 1, wx.ALIGN_LEFT | wx.LEFT, 5)
        self.birthdayText = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, style=wx.adv.DP_DROPDOWN)
        self.birthdayText.SetValue(wx.DateTime.Now())
        self.birthdayText.SetRange(wx.DateTime(1, 1, year=1900), wx.DateTime.Now())

        hbox2.Add(self.birthdayText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.TOP, 5)
        verticalBoxSizer.Add(hbox2)

        diagnosisBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        diagnosisLabel = wx.StaticText(panel, -1, "Диагноз", size=(170, 25))
        diagnosisBoxSizer.Add(diagnosisLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT, 5)

        self.diagnosisText = wx.TextCtrl(panel, size=(220, 25))
        diagnosisBoxSizer.Add(self.diagnosisText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.TOP, 5)
        dummyLabel = wx.StaticText(panel, -1, "", size=(150, 25))
        diagnosisBoxSizer.Add(dummyLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(diagnosisBoxSizer)

        operationBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        operationLabel = wx.StaticText(panel, -1, "Информация об оперативном вмешательстве", size=(170, 30))
        operationBoxSizer.Add(operationLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT, 5)

        self.operationText = wx.TextCtrl(panel, size=(220, 25))
        operationBoxSizer.Add(self.operationText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.TOP , 5)
        dummyLabel1 = wx.StaticText(panel, -1, "", size=(150, 25))
        operationBoxSizer.Add(dummyLabel1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(operationBoxSizer)

        helpDoctorBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpDoctorLabel = wx.StaticText(self, label="Заполните информацию о враче")
        helpDoctorBoxSizer.Add(self.helpDoctorLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        verticalBoxSizer.Add(helpDoctorBoxSizer)

        doctorFioBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        doctorFioLabel = wx.StaticText(panel, -1, "ФИО врача", size=(170, 25))
        doctorFioBoxSizer.Add(doctorFioLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT, 5)

        self.doctorFioText = wx.TextCtrl(panel, size=(220,25))
        doctorFioBoxSizer.Add(self.doctorFioText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.TOP , 5)
        self.doctorFioText.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        doctorFioExLabel = wx.StaticText(panel, -1, "пр. Иванов Иван Иванович", size=(150, 25))
        doctorFioBoxSizer.Add(doctorFioExLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(doctorFioBoxSizer)

        doctorPositionBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        doctorPositionLabel = wx.StaticText(panel, -1, "Должность врача", size=(170, 25))
        doctorPositionBoxSizer.Add(doctorPositionLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT, 5)

        self.doctorPositionText = wx.TextCtrl(panel, size=(220,25))
        doctorPositionBoxSizer.Add(self.doctorPositionText, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.TOP, 5)
        dummyLabel2 = wx.StaticText(panel, -1, "", size=(150, 25))
        doctorPositionBoxSizer.Add(dummyLabel2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        verticalBoxSizer.Add(doctorPositionBoxSizer)

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
        if str.isalpha(fio_parts[0]) is False:
            self.error_message = "Фамилия должна содержать только буквы!"
            dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                          style=wx.OK | wx.CENTRE).ShowModal()
            print("Please enter valid second name")
            return
        if str.isalpha(fio_parts[1]) is False:
            self.error_message = "Имя должно содержать только буквы!"
            dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                      style=wx.OK | wx.CENTRE).ShowModal()
            print("Please enter valid first name")
            return
        self.patient.secondName = fio_parts[0]
        self.patient.firstName = fio_parts[1]
        if len(fio_parts) > 3 or len(fio_parts) == 3:
            if len(fio_parts) > 3:
                self.error_message = "Введено слишком много слов, берутся первые три"
                dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                          style=wx.OK | wx.CENTRE).ShowModal()
                print("Too many words, truncating to first 3")
            if str.isalpha(fio_parts[2]) is False:
                self.error_message = "Отчество должно содержать только буквы!"
                dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                          style=wx.OK | wx.CENTRE).ShowModal()
                print("Please enter valid middle name")
                return
            self.patient.middleName = fio_parts[2]

        self.patient.birthday = self.birthdayText.GetValue().Format("%d.%m.%Y")

        self.patient.testDay = self.t4.GetValue()

        doctorFio = self.doctorFioText.GetValue()

        if not doctorFio:
            doctorFio = DEFAULT_DOCTOR_FIO

        doctorFio_parts = doctorFio.split()

        if str.isalpha(doctorFio_parts[0]) is False:
            self.error_message = "Фамилия должна содержать только буквы!"
            dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                      style=wx.OK | wx.CENTRE).ShowModal()
            print("Please enter valid second name")
            return
        if str.isalpha(doctorFio_parts[1]) is False:
            self.error_message = "Имя должно содержать только буквы!"
            dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                      style=wx.OK | wx.CENTRE).ShowModal()
            print("Please enter valid first name")
            return
        self.patient.doctorSecondName = doctorFio_parts[0]
        self.patient.doctorFirstName = doctorFio_parts[1]
        if len(doctorFio_parts) > 3 or len(doctorFio_parts) == 3:
            if len(doctorFio_parts) > 3:
                self.error_message = "Введено слишком много слов, берутся первые три"
                dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                          style=wx.OK | wx.CENTRE).ShowModal()
            if str.isalpha(doctorFio_parts[2]) is False:
                self.error_message = "Отчество должно содержать только буквы!"
                dialog = wx.MessageDialog(self.parent, self.error_message, caption="Ошибка ввода данных",
                                          style=wx.OK | wx.CENTRE).ShowModal()
                print("Please enter valid middle name")
                return
            self.patient.doctorMiddleName = doctorFio_parts[2]

        position = self.doctorPositionText.GetValue()

        diagnosis = self.diagnosisText.GetValue()
        self.patient.diagnosis = diagnosis

        operation = self.operationText.GetValue()
        self.patient.operation = operation

        if not position:
            position = DEFAULT_DOCTOR_POSITION
        self.patient.doctorPosition = position

        print(self.patient.birthday)
        print(self.patient.secondName)
        print(self.patient.firstName)
        print(self.patient.middleName)
        print(self.patient.doctorSecondName)
        print(self.patient.doctorFirstName)
        print(self.patient.doctorMiddleName)

        self.Hide()
        next_panel = self.parent.session_settings
        next_panel.update()
        next_panel.Show()
        self.Layout()

