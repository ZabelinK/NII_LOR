from patient_info_panel import *
from audio_choosing_panel import *
from patient_testing_panel import *
from patient_result_panel import *
from recognition_simple_panel import *
import itertools

class MainFrame(wx.Frame):
    def __init__(self, patient_testing_model, recognition_service_settings, test_settings):
        wx.Frame.__init__(self, None, wx.ID_ANY, "НИИ ЛОР - Тестирование звука")

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)
        self.all_panels_in_order = []

        # Creating all panels
        self.record_audio = self.addPanel(RecognitionSimplePanel(self, recognition_service_settings=recognition_service_settings))

        self.patient_info = self.addPanel(PatientInfoPanel(self, testing_model=patient_testing_model))

        self.audio_choosing = self.addPanel(AudioChoosingPanel(self, testing_model=patient_testing_model, 
                                                               test_setting=test_settings))

        self.patient_testing = self.addPanel(PatientTestingPanel(self, testing_model=patient_testing_model, 
                                                                 test_settings=test_settings,
                                                                 recognition_service_setting=recognition_service_settings))

        self.patient_result_panel = self.addPanel(PatientResultPanel(self, testing_model=patient_testing_model))


        self.current_panel = itertools.cycle(self.all_panels_in_order)

        # Add them to sized and hide all except first
        for panel in self.all_panels_in_order:
            sizer.Add(panel, 1, wx.EXPAND)

            if panel != self.record_audio:
                panel.Hide()

    def addPanel(self, panel):
        self.all_panels_in_order.append(panel)
        return panel
