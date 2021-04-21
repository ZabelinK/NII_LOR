import os
import wx
import wx.media
import wx.lib.buttons as buttons

import sounddevice as sd
import soundfile as sf
import numpy as np
import requests
import json 


dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')
########################################################################
class MediaPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        
        self.frame = parent
        self.currentVolume = 50
        self.layoutControls()
        
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        
        # record parameters
        self.fs = 8000
        self.data = np.empty([1, 2])
        self.wav_name = "../workdir/out.wav"
        self.recognize_service = 'https://asr.kube.plintum.dev/recognize?lang=ru'
        
    #----------------------------------------------------------------------
    def layoutControls(self):
        """
        Create and layout the widgets
        """
        
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
                
        self.recordBtn = wx.ToggleButton(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать запись")
        self.recordBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onRecord)

        self.textRes = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP, 
            value="", name="Результаты распознавания", size=(400, 500))

        # Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.VERTICAL)
                
        # layout widgets
        hSizer.Add(self.recordBtn, 0, wx.ALL, 5)
        hSizer.Add(self.textRes, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
        
        self.SetSizer(mainSizer)
        self.Layout()

    def saveDataToWav(self):
        """
        Save audio data to wav file
        """

        sf.write(self.wav_name, self.data, self.fs)

    def recognizeWav(self):
        """
        Open wav file and send reques to recognizion service to recognize audio data
        """

        with open(self.wav_name, "rb") as binaryfile :
            wav_data = bytearray(binaryfile.read())

        print("Data saved to {}".format(self.wav_name))

        rsp = requests.post(self.recognize_service, data = wav_data)

        print("Response from recognize service {}".format(str(rsp)))
        try:
            return json.loads(rsp.text)["text"]
        except Exception as e:
            print(rsp)
            print(e)
            return None

    def startRecord(self):
        """
        Start record from micro
        """
        def callback(indata, frames, time, status):
            self.data = np.append(self.data, indata, axis=0)

        self.data = np.empty([1, 2])
        self.stream = sd.InputStream(samplerate=self.fs, channels=2, callback=callback)
        self.stream.start()
        print("Start recording")
    
    def stopRecord(self):
        """
        Stop Record
        """
        self.stream.stop()
        print("Stop Recording")
        self.saveDataToWav()
        text = self.recognizeWav()

        print("Result : {}".format(text))

        self.textRes.Clear()
        if text is None:
            self.textRes.write("< Произошла ошибка, подробности в консоли >")
        else:
            self.textRes.write(text)

    def onRecord(self, event):
        """
        Start and stop record
        """

        if self.recordBtn.GetValue() == True:
            self.recordBtn.SetLabel("Остановить запись")
            self.startRecord()

        else:
            self.recordBtn.SetLabel("Начать запись")
            self.recordBtn.Disable()
            self.stopRecord()
            self.recordBtn.Enable()

########################################################################
class MediaFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "НИИ ЛОР - Тестирование звука")
        panel = MediaPanel(self)
        
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()