import os
import wx
import wx.media
import wx.grid
import wx.lib.scrolledpanel as scrolled
import csv
import numpy as np
import matplotlib.pyplot  as plt

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, '../../bitmaps')

class IntensityGraphPanel(scrolled.ScrolledPanel):

    def __init__(self, parent, testing_model, test_settings, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model
        self.test_settings = test_settings
        self.recognition_service_settings = recognition_service_settings

        self.current_testing_item = 0

        self.frame = parent
        self.SetSize((900, 800))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def layoutControls(self):
        wx.InitAllImageHandlers()

        self.intensitySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.intensityLabel = wx.StaticText(self, label="Интенсивность: ", size=(100, 20))
        self.intensityTexts = []

        for i in range(10):
            self.intensityText= wx.TextCtrl(self, size=(55, 20))
            self.intensityTexts.append(self.intensityText)

        self.intensitySizer.Add(self.intensityLabel, 0, wx.ALL, 5)

        for i in range(10):
            self.intensitySizer.Add(self.intensityTexts[i], 0, wx.ALL, 5)

        self.scoreSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scoreLabel = wx.StaticText(self, label="Разборчивость: ", size=(100, 20))
        self.scoreTexts = []

        for i in range(10):
            self.scoreText= wx.TextCtrl(self, size=(55, 20))
            self.scoreTexts.append(self.scoreText)

        self.scoreSizer.Add(self.scoreLabel, 0, wx.ALL, 5)

        for i in range(10):
            self.scoreSizer.Add(self.scoreTexts[i], 0, wx.ALL, 5)

        self.intensityBtn = wx.Button(self, style=wx.SL_VERTICAL | wx.SL_INVERSE, label="Добавить", size=(120, 30))
        self.intensityBtn.Bind(wx.EVT_BUTTON, self.updateGraph)
        self.intensitySizer.Add(self.intensityBtn, 0, wx.ALL, 5)

        self.backBtn = wx.Button(self, style=wx.SL_VERTICAL | wx.SL_INVERSE, label="Назад", size=(120, 30))
        self.backBtn.Bind(wx.EVT_BUTTON, self.back)
        self.scoreSizer.Add(self.backBtn, 0, wx.ALL, 5)

        self.imageSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.imageCtrl = wx.StaticBitmap(self)
        self.imageSizer.AddSpacer(110)
        self.imageSizer.Add(self.imageCtrl)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.intensitySizer)
        self.mainSizer.Add(self.scoreSizer)
        self.mainSizer.Add(self.imageSizer, 0, wx.ALL, 5)
        self.updateGraph(self)
        self.SetSizer(self.mainSizer)
        self.Layout()

    def back(self, event):
        self.Hide()
        self.parent.current_panel = self.parent.patient_result_panel
        next_panel = self.parent.current_panel
        next_panel.Show()
        self.Layout()

    def updateGraph(self, event):
        plt.close()
        f = open('intensity.csv', 'w')
        fieldnames = ['intensity', 'score']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        for i in range(10):
            writer.writerow({'intensity': self.intensityTexts[i].GetValue(), 'score': self.scoreTexts[i].GetValue()})
        f.close()

        data = np.genfromtxt("intensity.csv", delimiter=",", names=["x", "y"])

        plt.xlabel('Интенсивность (dB)', color='gray')
        plt.ylabel('Разборчивость (%)', color='gray')
        plt.grid(True)
        plt.axis([0, 110, 0, 110])
        plt.plot(data['x'], data['y'], color='b')
        plt.savefig('intensity.png')
        img = wx.Image("./intensity.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.imageCtrl.SetBitmap(wx.Bitmap(img))

    def nextPanel(self, event):
        self.parent.SetSize(self.prev_size)
        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()
