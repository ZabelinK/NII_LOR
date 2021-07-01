import wx
import sys

import main_panels.main_frame as mf
import models.patient_testing_model as ptm
from utils.error_handling import exception_logger

if __name__ == "__main__":
    patient_testing_model = ptm.PatientTestingModel()
    print(sys.argv[3])
    try:
        recognition_service_settings = ptm.RecognitionServiceSettings(sys.argv[1], sys.argv[2], sys.argv[3],
                                                                      sys.argv[4], sys.argv[5], sys.argv[6])
        test_settings = ptm.TestSettings()
        application = wx.App(False)
        main_frame = mf.MainFrame(patient_testing_model, recognition_service_settings, test_settings)
        main_frame.Show()
        application.MainLoop()
    except Exception as e:
        exception_logger(e)