from patient_info_panel import *
from audio_choosing_panel import *
from patient_testing_panel import *
from patient_result_panel import *
from recognition_simple_panel import *
import itertools

class MainFrame(wx.Frame):
    def __init__(self, patient_testing_model, recognition_service_settings, test_settings):
        wx.Frame.__init__(self, None, wx.ID_ANY, "НИИ ЛОР - Речевая аудиометрия", size=(640, 480))

        self.recognition_service_settings = recognition_service_settings
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        checkItem = fileMenu.Append(wx.ID_ANY, 'Проверить сервис распознавания речи')
        aboutItem = fileMenu.Append(wx.ID_ANY, 'О программе')
        exitItem = fileMenu.Append(wx.ID_EXIT, 'Выход', 'Выйти из приложения')
        menubar.Append(fileMenu, '&Файл')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnCheck, checkItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, exitItem)

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

    def OnCheck(self, e):
        self.next_frame = CheckFrame(self.recognition_service_settings)

    def OnAbout(self, e):
        self.Close()

    def OnQuit(self, e):
        self.Close()

class CheckFrame(wx.Frame):
    def __init__(self, recognition_service_settings):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Cервис распознавания речи", size=(640, 480))
        panel = RecognitionSimplePanel(self, recognition_service_settings=recognition_service_settings)
        self.Show()
