import os
import wx
import wx.media

from patient_testing_model import *
from recognition_service import *
from microphone_service import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PatientResultPanel(wx.Panel):

    def __init__(self, parent, testing_model):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model

        self.SetSize((800, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()


    def layoutControls(self):
        wx.InitAllImageHandlers()

        self.helpLabel = wx.StaticText(self, label="PANEL FOR PATIENT'S RESULTS", size=(400, 90))

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Продолжить", size=(120, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.nextBtn)
        self.mainSizer.Add(self.helpLabel)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def nextPanel(self, event):
        self.Hide()
        next(self.parent.current_panel).Show()
        self.Layout()
