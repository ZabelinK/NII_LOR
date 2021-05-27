from patient_info_panel import *
from audio_choosing_panel import *
from patient_testing_panel import *
from patient_result_panel import *
from recognition_simple_panel import *
from about_panel import *
from constants import *

import itertools
import webbrowser

class MainFrame(wx.Frame):
    def __init__(self, patient_testing_model, recognition_service_settings, test_settings):
        wx.Frame.__init__(self, None, wx.ID_ANY, "НИИ ЛОР - Речевая аудиометрия", size=(640, 480))

        self.recognition_service_settings = recognition_service_settings

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        checkItem = fileMenu.Append(wx.ID_ANY, 'Проверить сервис распознавания речи')
        exitItem = fileMenu.Append(wx.ID_EXIT, 'Выход', 'Выйти из приложения')
        menubar.Append(fileMenu, '&Файл')
        editMenu = wx.Menu()
        settingsItem = editMenu.Append(wx.ID_ANY, 'Настройки')
        menubar.Append(editMenu, '&Правка')
        helpMenu = wx.Menu()
        helpItem = helpMenu.Append(wx.ID_ANY, 'Открыть руководство пользователя')
        aboutItem = helpMenu.Append(wx.ID_ANY, 'О программе')
        menubar.Append(helpMenu, '&Помощь')


        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnCheckService, checkItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnHelp, helpItem)
        self.Bind(wx.EVT_MENU, self.OnSettings, settingsItem)

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)
        self.all_panels_in_order = []

        # Creating all panels
        self.patient_info = self.addPanel(PatientInfoPanel(self, testing_model=patient_testing_model))

        self.audio_choosing = self.addPanel(AudioChoosingPanel(self,
                                                               testing_model=patient_testing_model,
                                                               test_setting=test_settings,
                                                               recognition_service_settings=recognition_service_settings))

        self.patient_testing = self.addPanel(PatientTestingPanel(self, testing_model=patient_testing_model, 
                                                                 test_settings=test_settings,
                                                                 recognition_service_settings=recognition_service_settings))

        self.patient_result_panel = self.addPanel(PatientResultPanel(self, testing_model=patient_testing_model, 
                                                                     test_settings=test_settings,
                                                                     recognition_service_settings=recognition_service_settings))


        self.current_panel = itertools.cycle(self.all_panels_in_order)

        # Add them to sized and hide all except first
        show_panel = next(self.current_panel)
        for panel in self.all_panels_in_order:
            sizer.Add(panel, 1, wx.EXPAND)

            if panel != show_panel:
                panel.Hide()


    def addPanel(self, panel):
        self.all_panels_in_order.append(panel)
        return panel

    def OnCheckService(self, e):
        self.next_frame = CheckFrame(self.recognition_service_settings)

    def OnAbout(self, e):
        self.next_frame = AboutFrame("")

    def OnHelp(self, e):
        help_file = PATH_TO_DOCS + '"Руководство пользователя.docx"'
        os.system('start ' + help_file)

    def OnSettings(self, e):
        self.next_frame = ErrorFrame("")

    def OnQuit(self, e):
        self.Close()

class CheckFrame(wx.Frame):
    def __init__(self, recognition_service_settings):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Проверка сервиса распознавания речи", size=(640, 480))
        panel = RecognitionSimplePanel(self, recognition_service_settings=recognition_service_settings)
        self.Show()

class ErrorFrame(wx.Frame):
    def __init__(self, error_message):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Настройки")
        panel = ErrorPanel(self, message="")
        self.Show()

class AboutFrame(wx.Frame):
    def __init__(self, error_message):
        wx.Frame.__init__(self, None, wx.ID_ANY, "О программе")
        panel = AboutPanel(self, message="")
        self.Show()