import wx
import sys
from patient_testing_model import *

from main_frame import *

if __name__ == "__main__":
    patient_testing_model = PatientTestingModel()
    recognition_service_settings = RecognitionServiceSettings(sys.argv[1])
    test_settings = TestSettings()

    application = wx.App(False)

    main_frame = MainFrame(patient_testing_model, recognition_service_settings, test_settings)
    main_frame.Show()

    application.MainLoop()