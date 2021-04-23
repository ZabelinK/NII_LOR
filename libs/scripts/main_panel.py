import wx
import wx.media
from patient_info_panel import *
from audio_choosing_panel import *
from patient_testing_panel import *
from patient_result_panel import *
from application import *
import sys

from patient_testing_model import *
from recognition_service import *
from microphone_service import *

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "НИИ ЛОР - Тестирование звука")

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        self.all_panels = []

        # Creating all panels
        self.patient_result_panel = self.addPanel(PatientResultPanel(self, next_panel=None))
        self.patient_testing = self.addPanel(PatientTestingPanel(self, next_panel=self.patient_result_panel))
        self.audio_choosing = self.addPanel(AudioChoosingPanel(self, next_panel=self.patient_testing))
        self.patient_info = self.addPanel(PatientInfoPanel(self, next_panel=self.audio_choosing))
        self.record_audio = self.addPanel(MediaPanel(self, next_panel=self.patient_info, 
            recognition_service_settings=recognition_service_settings))
        self.patient_result_panel.next_panel = self.record_audio

        self.current_panel = self.record_audio


        # Add them to sized and hide all except first
        for panel in self.all_panels:
            sizer.Add(panel, 1, wx.EXPAND)

            if panel != self.current_panel:
                panel.Hide()

    def addPanel(self, panel):
        self.all_panels.append(panel)
        return panel

if __name__ == "__main__":
    patient_testing_model = PatientTestingModel()
    test_settings = TestSettings()
    recognition_service_settings = RecognitionServiceSettings(sys.argv[1])

    application = wx.App(False)

    main_frame = MainFrame()
    main_frame.Show()

    application.MainLoop()