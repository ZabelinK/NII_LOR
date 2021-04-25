import os
import wx
import wx.media

import patient_testing_model
from patient_testing_model import *
from recognition_service import *
from microphone_service import *
from wx.lib.pubsub import pub

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PatientTestingPanel(wx.Panel):

    def __init__(self, parent, next_panel):
        wx.Panel.__init__(self, parent=parent)
        pub.subscribe(self.myListener, "panelListener")

        self.frame = parent
        self.SetSize((800, 600))
        self.layoutControls()
        self.next_panel = next_panel
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        self.patient = patient_testing_model.PatientTestingModel()

    def myListener(self, message):
        self.patient = message
        print("hi from next panel")
        print(self.patient.birthday)

    def layoutControls(self):
        wx.InitAllImageHandlers()

        self.helpLabel = wx.StaticText(self, label="PANEL FOR TESTING PATIENT", size=(400, 90))

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Продолжить", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.nextBtn)
        self.mainSizer.Add(self.helpLabel)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def nextPanel(self, event):
        if self.next_panel == None:
            return
        
        self.Hide()
        self.next_panel.Show()
        self.Layout()
